"""Ingests historical CSV data into DB"""

import argparse
import asyncio
import logging
import textwrap

from aiohttp import ClientSession
import pandas as pd
import daiquiri

daiquiri.setup(level=logging.INFO)
log = daiquiri.getLogger(__name__) # pylint: disable=invalid-name

async def _ingest_probable_cve(json_obj, session: ClientSession, url):
    async with session.post(url, json=json_obj) as response:
        log.info('Got response {} for {}'.format(response.status, url))

async def _add_feedback(json_obj, session: ClientSession, url):# pylint: disable=unused-argument
    # (todo) add feedback
    pass

def _get_executor(args):
    if args.ingestion_endpoint:
        return _ingest_probable_cve, args.ingestion_endpoint
    return _add_feedback, args.feedback_endpoint

async def _main(args):
    log.info('invoking ingestion for {} CSV files'.format(len(args.csv)))
    func, url = _get_executor(args)
    for csv in args.csv:
        log.info('Convert records in {} to JSON'.format(csv))
        obj = pd.read_csv(csv, index_col=None, header=0).to_dict(orient='records')
        log.info('Ingest {} records to DB'.format(len(obj)))
        async with ClientSession() as session:
            await func(json_obj=obj, session=session, url=url)

def _parse_args():
    parser = argparse.ArgumentParser(prog='python',
                                     description=textwrap.dedent('''\
                                    This script can be used to ingest historical CSV data
                                    into database using API'''))
    parser.add_argument("--csv",
                        help="Glob path of CSV files which has to be ingested into DB",
                        nargs="+",
                        required=True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--ingestion-endpoint", type=str,
                       default="http://localhost:5000/api/v1/pcve",
                       help="Ingestion API endpoint")
    group.add_argument("--feedback-endpoint", type=str,
                       default="http://localhost:5000/api/v1/feedback",
                       help="Feedback API endpoint")
    return parser.parse_args()

if __name__ == '__main__':
    # pylint: disable=invalid-name
    loop = asyncio.get_event_loop()
    # (todo) Use asyncio.run after moving to Python 3.7+
    try:
        loop.run_until_complete(_main(args=_parse_args()))
    finally:
        loop.close()
