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


async def _insert_df(df, url, csv, sem):  # pylint: disable=invalid-name
    objs = df.to_dict(orient='records')
    tasks = []
    async with ClientSession() as session:
        for obj in objs:
            task = asyncio.ensure_future(_add_data(obj=obj, session=session, url=url, csv=csv, sem=sem))
            tasks.append(task)
        await asyncio.gather(*tasks)


async def _add_data(obj, session: ClientSession, url, csv, sem):
    async with sem, session.post(url, json=obj) as response:
        log.debug('Got response {} for {}'.format(response.status, obj))
        if response.status != 200:
            log.error('Error response {}, msg {}, for {}'.format(response.status, await response.text(), obj))
            _failing_list.update(dict([(csv, response.status)]))


async def _add_feedback(df, url, csv, sem):  # pylint: disable=invalid-name
    if len(df) < 1:
        return

    log.debug('Feedback record count {count}'.format(count=len(df)))

    # filter data with probable_cve as true, for them only need to add feedback
    is_probable_cve = True  # need to declare into variable to fix pylint error
    df = df.loc[df['probable_cve'] == is_probable_cve]
    log.debug('Filtered feedback record count {count}'.format(count=len(df)))

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
    await _insert_df(df, url, csv, sem)


def _get_executor(args):
    if args.feedback:
        return _add_feedback, args.feedback
    return _insert_df, args.insert


def _get_status_type(status: str) -> str:
    if status.lower() in ['opened', 'closed', 'reopened']:
        return status.upper()
    else:
        return "OTHER"


def _get_probabled_cve(cve_model_flag: int) -> bool:
    return True if cve_model_flag is not None and cve_model_flag == 1 else False


def _dedupe_data(df: pd.DataFrame) -> pd.DataFrame:
    # Dedupe check - If similar records present multiple time then take latest record based on updated_at.
    df['converted_updated_at'] = pd.to_datetime(df.updated_at)
    df = df.loc[df.groupby('url').converted_updated_at.idxmax(skipna=False)].reset_index(drop=True)
    df = df.drop(columns=['converted_updated_at'])
    return df


def _update_df(df: pd.DataFrame) -> pd.DataFrame:
    df['ecosystem'] = df['ecosystem'].str.upper()
    df['status'] = df.apply(lambda x: _get_status_type(x['status']), axis=1)

    if 'cve_model_flag' not in df:
        df['probable_cve'] = True
    else:
        df['probable_cve'] = df.apply(lambda x: _get_probabled_cve(x['cve_model_flag']), axis=1)

    df = _dedupe_data(df)

    return df.where(pd.notnull(df), None)


async def _main(args):
    daiquiri.setup(level=("DEBUG" if args.verbose else "INFO"))
    log.info('invoking ingestion for {} CSV files'.format(len(args.csv)))
    func, url = _get_executor(args)
    sem = asyncio.BoundedSemaphore(args.concurrency)
    for csv in args.csv:
        log.debug('Convert records in {} to JSON'.format(csv))
        df = pd.read_csv(csv, index_col=None, header=0)  # pylint: disable=invalid-name
        log.debug('CSV Record count {count}'.format(count=len(df)))
        updated_df = _update_df(df)
        # Runnning one file at a time to overcome duplicate issue for similar record across different ecosystem
        # though all data inside dataframe/file will be inserted parallel
        await func(df=updated_df, url=url, csv=csv, sem=sem)

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
