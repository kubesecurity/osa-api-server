"""Load sample bulk data using this script."""
import json
import pprint
import random
import string
import threading
import time
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from datetime import datetime, timedelta

import daiquiri
import requests

daiquiri.setup(level="INFO")
log = daiquiri.getLogger(__name__)  # pylint: disable=invalid-name

"""
Configure below variables, which are used in test data
"""
# Host URL where we can fire all api request
HOST_URL = "http://localhost:5000"
# No of total data we wanted to ingest
NO_OF_REQUEST = 10
# index used to create unique url (You can change it if you have already data available for earlier trest run)
START_INDEX = 1
# max no of request those can run parallel
WORKER_COUNT = 3


INGEST_DATA_URL = "{host}/api/v1/pcve".format(host=HOST_URL)
ADD_FEDDBACK_URL = "{host}/api/v1/feedback".format(host=HOST_URL)

threadLock1 = threading.Lock()
threadLock2 = threading.Lock()

ids = [*range(START_INDEX, START_INDEX + NO_OF_REQUEST)]

ecosystems = ['OPENSHIFT', 'KNATIVE', 'KUBEVERT', 'OPENSHIFT']

repo_names = []
for i in range(1, 50):
    for j in range(1, 20):
        repo_names.append('org{ord_id}/repo{repo_id}'.format(ord_id=i, repo_id=j))

event_types = ["ISSUE", "PULL_REQUEST"]

issue_ids = [*range(1000, 10000)]

days = [*range(0, 1000)]
dates = []

for i in range(1, 1000):
    # N = random.choice(days)
    date_N_days_ago = datetime.now() - timedelta(days=i)
    dates.append(date_N_days_ago.strftime('%Y-%m-%d %H:%M:%S+00:00'))

creator_names = []
for index in range(1, 200):
    creator_names.append("user{id}".format(id=index))

feedback_type = ["POSITIVE", "NEGATIVE"]
feedback_count = [0, 1, 2, 3]

headers = {'Content-type': 'application/json'}

# bansed on existing data given opned/closed to more weightage, same for robable cve data given low weightage
statuses = ['OPENED', 'CLOSED', 'REOPENED', 'OPENED', 'CLOSED']
probable_cve = [True, True, False, False, False, False, False, False]


def update_data(request_id):
    """Create sample json with help of raw_data."""
    raw_data = {"api_url": "https://api.github.com/repos/org2/repo2/issues/1", "closed_at": "2019-11-08 21:14:39+00:00",
                "created_at": "2019-11-08 00:19:12+00:00", "creator_name": "user7",
                "creator_url": "https://github.com/user7", "event_type": "PullRequestEvent",
                "id": 1, "number": 3342, "repo_name": "org2/repo2", "status": "closed", "ecosystem": "openshift",
                "updated_at": "2019-11-08 21:14:39+00:00", "url": "https://github.com/org2/repo2/issues/1"}

    log.info("Calling for request {no}".format(no=request_id))
    repo_name = random.choice(repo_names)
    creator_name = random.choice(creator_names)

    url = "https://github.com/{repo_name}/issues/{issue}"
    api_url = "https://api.github.com/repos/{repo_name}/issues/{issue}"
    raw_data["url"] = url.format(repo_name=repo_name, issue=request_id)
    raw_data["ecosystem"] = random.choice(ecosystems)
    raw_data["event_type"] = random.choice(event_types)
    raw_data["id"] = request_id
    raw_data["number"] = random.choice(issue_ids)
    raw_data["repo_name"] = repo_name
    raw_data["api_url"] = api_url.format(repo_name=repo_name, issue=request_id)
    raw_data['created_at'] = random.choice(dates)
    raw_data['updated_at'] = random.choice(dates)
    raw_data['closed_at'] = random.choice(dates)
    raw_data["creator_name"] = creator_name
    raw_data["creator_url"] = "https://github.com/{user}".format(user=creator_name)
    raw_data['probable_cve'] = random.choice(probable_cve)
    raw_data['status'] = random.choice(statuses)
    ingest_data(request_id, raw_data)


def insert_feedback(thread_no, url):
    """Insert feedback."""
    raw_feedback = {"author": "string", "comments": "string", "url": "string", "feedback_type": "POSITIVE",
                    "identified_cve": "string"}
    feedback_random_count = random.choice(feedback_count)
    while feedback_random_count > 0:
        raw_feedback['author'] = random.choice(creator_names)
        raw_feedback['comments'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        raw_feedback['url'] = url
        raw_feedback['feedback_type'] = random.choice(feedback_type)
        raw_feedback['identified_cve'] = "csv{id}".format(id=thread_no)
        resp = requests.post(url=ADD_FEDDBACK_URL, data=json.dumps(raw_feedback), headers=headers)
        if resp.status_code != 200:
            log.info("Failed to add feedback for {id}, code:{code}, msg:{msg}".format(id=thread_no,
                                                                                   code=str(resp.status_code),
                                                                                   msg=resp.json().get("message")))
            log.info('Request Failed------Start-------')
            pprint.pprint(json.dumps(raw_feedback))
            log.info('Request Failed------End-------')
        feedback_random_count = feedback_random_count - 1


def ingest_data(thread_no, payload_temp):
    """Ingest sample security event."""
    resp = requests.post(url=INGEST_DATA_URL, data=json.dumps(payload_temp), headers=headers)
    if resp.status_code == 200:
        with threadLock1:
            global count
            count += 1
        if payload_temp['probable_cve'] is True:
            insert_feedback(thread_no, payload_temp['url'])
    else:
        log.info("Failed to ingest data for {id}, code:{code}, msg:{msg}".format(id=thread_no,
                                                                              code=str(resp.status_code),
                                                                              msg=resp.json().get("message")))
        log.info('Request Failed------Start-------')
        pprint.pprint(json.dumps(payload_temp))
        log.info('Request Failed------End-------')


count = 0


def run_ingest_job():
    """Run actual job to ingest sample buld data."""
    # start timer
    t0 = time.perf_counter()

    with PoolExecutor(max_workers=WORKER_COUNT) as executor:
        while len(ids) > 0 or count == 500:
            with threadLock2:
                current_id = ids.pop(0)
                executor.submit(update_data, current_id)

    # end timer
    t1 = time.perf_counter()

    log.info("total request succeed {count}".format(count=str(count)))
    log.info(f"Total time taken to insert {NO_OF_REQUEST} are {t1 - t0:0.4f} seconds")


run_ingest_job()
