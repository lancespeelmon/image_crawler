#!/usr/bin/env python3

#############################################################################
# FIXME this async implementation _works_ but has some major logging issues #
#############################################################################

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

from crawler.config import CrawlerConfig
from crawler.crawler import Crawler
from logger.logger import get_logger

LOGGER = get_logger()
CONFIG = CrawlerConfig(LOGGER)
CONCURRENCY = CONFIG.concurrency
LOGGER.debug("concurrency = %s", CONCURRENCY)
EXECUTOR = ThreadPoolExecutor(CONCURRENCY)


async def worker(name, queue):
    unit = await queue.get()
    crawler: Crawler = CONFIG.crawler(unit['crawler'])
    try:
        loop = asyncio.get_event_loop()
        (files_downloaded, exceptions) = await loop.run_in_executor(
            EXECUTOR, crawler.crawl, unit['targets'], render=unit['render'], ignore=unit['image_ignore_patterns'])
        LOGGER.info("Downloaded %s files", files_downloaded)
        if exceptions:
            LOGGER.error("found %s errors!", len(exceptions))
            for ex in exceptions:
                LOGGER.error(ex.message, ex)
    except Exception as ex:
        raise ex
    finally:
        # Notify the queue that the "work item" has been processed.
        queue.task_done()


async def main():
    # push our units of work onto the queue
    queue = asyncio.Queue(maxsize=CONCURRENCY)
    for unit in CONFIG.workload:
        queue.put_nowait(unit)

    tasks = []
    for i in range(CONCURRENCY):
        task = asyncio.create_task(worker(f'crawler-{i}', queue))
        tasks.append(task)

    # Wait until the queue is fully processed.
    started_at = time.monotonic()
    await queue.join()
    elasped_time = time.monotonic() - started_at

    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()

    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)

    LOGGER.info("Elapsed time: %.2f", elasped_time)


if __name__ == "__main__":
    asyncio.run(main())
