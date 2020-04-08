"""Populate graph schema."""

import time

import json
import os

import daiquiri
import requests

from src import config

daiquiri.setup(level=config.DAIQUIRI_LOG_LEVEL)
logger = daiquiri.getLogger(__name__)


def execute(str_gremlin_dsl):
    """Execute the query prepared for the graph database."""
    logger.info("Execute gremlin DSL : {dsl}".format(dsl=str_gremlin_dsl))
    payload = {'gremlin': str_gremlin_dsl}
    response = requests.post(config.GREMLIN_URL, data=json.dumps(payload))
    json_response = response.json()

    logger.info("Execute Response : {res}".format(res=response))
    if response.status_code != 200:
        logger.error("ERROR with code: {code}, reason: {reason}, msg: {msg}".format(code=str(response.status_code),
                                                                                    reason=response.reason,
                                                                                    msg=json_response.get("message")))
        return False, json_response
    else:
        return True, json_response


def populate_schema():
    """Populate the schema stored in the Groovy script."""
    current_file_path = os.path.dirname(os.path.realpath(__file__))
    schema_file_path = os.path.join(current_file_path, 'scripts/schema.groovy')
    str_gremlin_dsl = ''''''
    with open(schema_file_path, 'r') as f:
        str_gremlin_dsl = f.read()

    return execute(str_gremlin_dsl)


def run():
    """Populate graph schema."""
    logger.info('Populating graph schema...')

    status, json_result = populate_schema()
    if not status:
        logger.error(json_result)
        raise RuntimeError('Failed to setup graph schema')
    # to prevent weird "parallelMutate" errors
    time.sleep(10)


if __name__ == '__main__':
    run()
