"""Ingests historical CSV data into DB."""

from typing import Dict
import argparse
import asyncio
import textwrap

from aiohttp import ClientSession
import pandas as pd
import daiquiri

log = daiquiri.getLogger(__name__)  # pylint: disable=invalid-name

_failing_list: Dict[str, str] = {}


def _report_failures():
    if len(_failing_list) == 0:
        log.info("Successfully ingested")
    for k, v in _failing_list.items():  # pylint: disable=invalid-name
        log.error("'{}' failed with status '{}'".format(k, v))


async def _insert_df(df, session: ClientSession, url, csv, sem):  # pylint: disable=invalid-name
    objs = df.to_dict(orient='records')
    for obj in objs:
        async with sem, session.post(url, json=obj) as response:
            log.debug('Got response {} for {}'.format(response.status, obj))
            if response.status != 200:
                log.error('Error response {} for {}'.format(response.status, obj))
                _failing_list.update(dict([(csv, response.status)]))


async def _add_feedback(df, session: ClientSession, url, csv, sem):  # pylint: disable=invalid-name
    if len(df) < 1:
        return
    df['author'] = 'anonymous'
    # typo carried away
    for feedback in ('Feeedback', 'Feedback'):
        if feedback in df:
            df[feedback].fillna('', inplace=True)
            df.rename(columns=dict([(feedback, 'comments')]), inplace=True)
            break
    else:
        df['comments'] = ''
    # old feedback has false positives with comments, transform it to
    # POSITIVE or NEGATIVE
    tx_comment = lambda x: ('NEGATIVE' if x.lower().startswith('no') else 'POSITIVE')
    df['feedback_type'] = df['comments'].apply(tx_comment)
    df = df[['author', 'feedback_type', 'comments', 'url']]
    await _insert_df(df, session, url, csv, sem)


def _get_executor(args):
    if args.feedback:
        return _add_feedback, args.feedback
    return _insert_df, args.insert


async def _main(args):
    daiquiri.setup(level=("DEBUG" if args.verbose else "INFO"))
    log.info('invoking ingestion for {} CSV files'.format(len(args.csv)))
    func, url = _get_executor(args)
    sem = asyncio.BoundedSemaphore(args.concurrency)
    async with ClientSession() as session:
        tasks = []
        for csv in args.csv:
            log.debug('Convert records in {} to JSON'.format(csv))
            df = pd.read_csv(csv, index_col=None, header=0)  # pylint: disable=invalid-name
            log.debug('Ingest {} records to DB'.format(len(df)))
            task = asyncio.ensure_future(func(df=df, session=session, url=url,
                                              csv=csv, sem=sem))
            tasks.append(task)
        _ = await asyncio.gather(*tasks)
    _report_failures()


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
    parser.add_argument('--concurrency',
                        type=int,
                        default=10,
                        help='No of concurrent requests allowed')
    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help='increase output verbosity')
    return parser.parse_args()


if __name__ == '__main__':
    # pylint: disable=invalid-name
    loop = asyncio.get_event_loop()
    # (todo) Use asyncio.run after moving to Python 3.7+
    try:
        loop.run_until_complete(_main(args=_parse_args()))
    finally:
        loop.close()
