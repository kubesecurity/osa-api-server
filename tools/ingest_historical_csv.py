'''Ingests historical CSV data into DB'''

import argparse
import asyncio
import logging
import textwrap

from aiohttp import ClientSession
import pandas as pd
import daiquiri

daiquiri.setup(level=logging.INFO)
log = daiquiri.getLogger(__name__) # pylint: disable=invalid-name

async def _ingest_probable_cve(df, session: ClientSession, url): # pylint: disable=invalid-name
    obj = df.to_dict(orient='records')
    async with session.post(url, json=obj) as response:
        log.info('Got response {} for {}'.format(response.status, url))

async def _add_feedback(df, session: ClientSession, url): # pylint: disable=invalid-name
    if len(df) < 1:
        return
    df['author'] = 'anonymous'
    df['feedback_type'] = 'POSITIVE'
    # typo carried away
    for feedback in ('Feeedback', 'Feedback'):
        if feedback in df:
            df[feedback].fillna('', inplace=True)
            df.rename(columns=dict([(feedback, 'comments')]), inplace=True)
            break
    else:
        df['comments'] = ''
    df = df[['author', 'feedback_type', 'comments', 'url']]
    # df['comments'] = ''
    obj = df.to_dict(orient='records')
    async with session.post(url, json=obj) as response:
        log.info('Got response {} for {}'.format(response.status, url))

def _get_executor(args):
    if args.feedback:
        return _add_feedback, args.feedback
    return _ingest_probable_cve, args.insert

async def _main(args):
    log.info('invoking ingestion for {} CSV files'.format(len(args.csv)))
    func, url = _get_executor(args)
    for csv in args.csv:
        log.info('Convert records in {} to JSON'.format(csv))
        df = pd.read_csv(csv, index_col=None, header=0) # pylint: disable=invalid-name
        log.info('Ingest {} records to DB'.format(len(df)))
        async with ClientSession() as session:
            await func(df=df, session=session, url=url)

def _parse_args():
    parser = argparse.ArgumentParser(prog='python',
                                     description=textwrap.dedent('''\
                                    This script can be used to ingest historical CSV data
                                    into database using API'''))
    parser.add_argument('csv',
                        help='Glob path of CSV files which has to be ingested into DB',
                        nargs='+')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--insert',
                       type=str,
                       nargs='?',
                       const='http://localhost:5000/api/v1/pcve',
                       help='API endpoint to use for the operation')
    group.add_argument('--feedback',
                       type=str,
                       nargs='?',
                       const='http://localhost:5000/api/v1/feedback',
                       help='API endpoint to use for adding feedback')
    return parser.parse_args()

if __name__ == '__main__':
    # pylint: disable=invalid-name
    loop = asyncio.get_event_loop()
    # (todo) Use asyncio.run after moving to Python 3.7+
    try:
        loop.run_until_complete(_main(args=_parse_args()))
    finally:
        loop.close()
