#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import math
import logging
import sqlite3
import argparse
from collections import Counter
from multiprocessing import Queue, Process, Value, cpu_count

from helpers import mkdir_if_not_exists
from contexts import extract_context_from_doc_text


def extract_process(opts, i, jobs_queue, output_queue):
    """Pull tuples of raw page content, do CPU/regex-heavy fixup, push finished text
    :param i: process id.
    :param jobs_queue: where to get jobs.
    :param output_queue: where to queue extracted text for output.
    """

    global options
    options = opts
    sqlfile_path = options['sqlfile_path']
    job_batch_size = options['job_batch_size']
    createLogger(options['quiet'], options['debug'])

    while True:
        job = jobs_queue.get()  # job is (pageNum,)
        if job:
            pageNum, = job
            try:
                cv = Counter()
                wv = Counter()
                query = '''
                SELECT id, palavras
                FROM sentences
                WHERE palavras IS NOT NULL AND id > ?
                ORDER BY id
                LIMIT ?;
                '''
                with sqlite3.connect(sqlfile_path) as conn:
                    c = conn.cursor()
                    params = (pageNum * job_batch_size, job_batch_size)
                    batch_result = []
                    for (id, parsed_sentence,) in c.execute(query, params):
                        deps = []
                        for (word, context) in extract_context_from_doc_text(parsed_sentence):
                            wv.update([word])
                            cv.update([context])
                            deps.append([word, context])
                        batch_result.append((id, deps))

            except:
                cv, wv, batch_result = (None, None, None)
                logging.exception('Processing page: %s', pageNum)

            output_queue.put((pageNum, cv, wv, batch_result))
        else:
            logging.debug('Quit extractor')
            break

report_period = 10           # progress report period

def dump_counter(filename, counter):
    with open(filename, encoding='utf-8', mode='w', buffering = 65536) as f:
        for w, count in counter.items():
            f.write('{} {}\n'.format(w, count))

def reduce_process(opts, output_queue, spool_length):
    """Pull finished article text, write series of files (or stdout)
    :param opts: global parameters.
    :param output_queue: text to be output.
    :param spool_length: spool length.
    """

    global options
    options = opts
    output_dirname = options['output_dirname']
    createLogger(options['quiet'], options['debug'])

    wv_all = Counter()
    cv_all = Counter()

    with open(os.path.join(output_dirname, 'dep.contexts'), 'wb', 65536) as output:

        interval_start = time.perf_counter()
        # FIXME: use a heap
        spool = {}        # collected pages
        next_page = 1     # sequence numbering of page
        while True:
            if next_page in spool:
                result = spool.pop(next_page)
                cv, wv, batch_result = result
                if cv != None:
                    wv_all = wv_all + wv
                    cv_all = cv_all + cv
                    for (_, deps) in batch_result:
                        output.write(
                            ('\n'.join([' '.join(pair) for pair in deps])).encode('utf-8'))
                next_page += 1
                # tell mapper our load:
                spool_length.value = len(spool)
                # progress report
                if next_page % report_period == 0:
                    interval_rate = report_period / \
                        (time.perf_counter() - interval_start)
                    logging.info("Batch %d (%.1f batch/s)",
                                 next_page, interval_rate)
                    interval_start = time.perf_counter()
            else:
                # mapper puts None to signal finish
                pair = output_queue.get()
                if not pair:
                    dump_counter(os.path.join(output_dirname, 'wv'), wv_all)
                    dump_counter(os.path.join(output_dirname, 'cv'), cv_all)
                    break
                pageNum, cv, wv, batch_result = pair
                spool[pageNum] = (cv, wv, batch_result)
                # tell mapper our load:
                spool_length.value = len(spool)
                # FIXME: if an extractor dies, process stalls; the other processes
                # continue to produce pairs, filling up memory.
                if len(spool) > 200:
                    logging.debug('Collected %d, waiting: %d, %d', len(spool),
                                  next_page, next_page == pageNum)

def get_page_count(sqlfile_path, page_size):
    with sqlite3.connect(sqlfile_path) as conn:
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM sentences where palavras IS NOT NULL')
        (total,) = c.fetchone()
        return math.ceil(total/page_size)

def createLogger(quiet, debug):
    logger = logging.getLogger()
    if not quiet:
        logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)

def main():
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=__doc__)
    parser.add_argument("input", help="sqlfile_path")
    default_process_count = max(1, cpu_count() - 1)
    parser.add_argument("--processes", type=int, default=default_process_count,
                        help="Number of processes to use (default %(default)s)")
    parser.add_argument("-b", "--batchsize", type=int, default=50,
                        help="The number of sentences to be sended to the parser in each iteration.")
    parser.add_argument("-o", "--output", default="./data/contexts/",
                        help="directory for extracted files")

    groupS = parser.add_argument_group('Special')
    groupS.add_argument("-q", "--quiet", action="store_true",
                        help="suppress reporting progress info")
    groupS.add_argument("--debug", action="store_true",
                        help="print debug info")

    args = parser.parse_args()
    output_dirname = args.output
    mkdir_if_not_exists(output_dirname)
    sqlfile_path = args.input
    job_batch_size = args.batchsize

    FORMAT = '%(levelname)s: %(message)s'
    logging.basicConfig(format=FORMAT)

    options = {}
    options['quiet'] = args.quiet
    options['debug'] = args.debug
    options['sqlfile_path'] = sqlfile_path
    options['job_batch_size'] = job_batch_size
    options['output_dirname'] = output_dirname
    createLogger(options['quiet'], options['debug'])

    number_of_pages = get_page_count(sqlfile_path, job_batch_size)
    jobs = [(pageNum,) for pageNum in range(1, number_of_pages)]

    # process pages
    logging.info("Starting")
    extract_start = time.perf_counter()

    process_count = args.processes
    process_count = max(1, process_count)
    maxsize = 10 * process_count
    # output queue
    output_queue = Queue(maxsize=maxsize)
    worker_count = process_count

    # load balancing
    max_spool_length = 10000
    spool_length = Value('i', 0, lock=False)

    # reduce job that sorts and prints output
    reduce = Process(target=reduce_process,
                     args=(options, output_queue, spool_length))
    reduce.start()

    # initialize jobs queue
    jobs_queue = Queue(maxsize=maxsize)

    # start worker processes
    logging.info("Using %d processes.", worker_count)
    workers = []
    for i in range(worker_count):
        extractor = Process(target=extract_process,
                            args=(options, i, jobs_queue, output_queue))
        extractor.daemon = True  # only live while parent process lives
        extractor.start()
        workers.append(extractor)

    # Mapper process
    page_num = 0
    for page_data in jobs:
        pageNum, = page_data
        # slow down
        delay = 0
        if spool_length.value > max_spool_length:
            # reduce to 10%
            while spool_length.value > max_spool_length/10:
                time.sleep(10)
                delay += 10
        if delay:
            logging.info('Delay %ds', delay)
        job = (pageNum,)
        jobs_queue.put(job)  # goes to any available extract_process
        page_num += 1

    # signal termination
    for _ in workers:
        jobs_queue.put(None)
    # wait for workers to terminate
    for w in workers:
        w.join()

    # signal end of work to reduce process
    output_queue.put(None)
    # wait for it to finish
    reduce.join()

    extract_duration = time.perf_counter() - extract_start
    extract_rate = (page_num * job_batch_size) / extract_duration
    logging.info("Finished %d-process of %d sentences in %.1fs (%.1f sentences/s)",
                 process_count, page_num * job_batch_size, extract_duration, extract_rate)

if __name__ == '__main__':
    main()
