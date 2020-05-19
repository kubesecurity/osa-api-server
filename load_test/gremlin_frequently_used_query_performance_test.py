"""Class that contains logic to do performance test using Loctus framework."""

import logging
import random
from datetime import datetime, timedelta

from locust import HttpLocust, TaskSet, task, between

"""
https://locust.io/

You can simply install require dependency by using following command.
pip install locustio

Then you can run similar to below query.
locust -f gremlin_frequently_used_query_performance_test.py -c 5 -t=30m --no-web --loglevel debug \
--print-stats --logfile=output.log
-c: Number of concurrent Locust users. Only used togetherwith --no-web
-t: Stop after the specified amount of time, e.g. (300s,20m, 3h, 1h30m, etc.). Only used together with --no-web

Configure below variables, which are used in query to test data.
"""
QUERY_NO_OF_MONTH = 1
QUERY_NO_OF_DATE = 7
QUERY_NO_OF_REPO = 5
HOST_URL = "http://osa-api-server-{user}-fabric8-analytics.devtools-dev.ext.devshift.net/"
API_URL = "api/v1/graph"

ids = [*range(1, 10)]

repo_names = []
for i in range(1, 10):
    for j in range(1, 10):
        repo_names.append('org{ord_id}/repo{repo_id}'.format(ord_id=i, repo_id=j))

event_types = ["ISSUE", "PULL_REQUEST"]

issue_ids = [*range(1000, 10000)]

months = [201901, 201902, 201903, 201904, 201905, 201906, 201907, 201908, 201909, 201910, 201911, 201912]

dates = []
for i in range(1, 1000):
    # N = random.choice(days)
    date_N_days_ago = datetime.now() - timedelta(days=i)
    dates.append(int("{year}{month:02d}{date:02d}".format(year=date_N_days_ago.year, month=date_N_days_ago.month,
                                                          date=date_N_days_ago.day)))

repo_names = []
for i in range(1, 50):
    for j in range(1, 20):
        repo_names.append('org{ord_id}/repo{repo_id}'.format(ord_id=i, repo_id=j))

feedbacks = ["POSITIVE", "NEGATIVE", "NEUTRAL", "NONE"]

"""
Note: In below all gremlin query we are handcoding "ecosystem"=OPENSHIFT and "probable_cve"=true condition
- Taking ecosystem as "OPENSHIFT" as we have more data for OPENSHIFT compared to KNATIVE/KUBEVIRT
- External User will always see security_event with "probable_cve" as true.
"""


class QueryIngestedDataFequentlyUsedSteps(TaskSet):
    """Class that contains frequntly used query."""

    def _client_call(self, gremlin_query, name):
        headers = {'content-type': 'application/json'}
        with self.client.post(API_URL, json=gremlin_query, headers=headers, name=name) as response:
            logging.info('Query name: {name}, Status_code:{code}, No of data:{record_count}, Query:"{query}"'
                         .format(name=name, query=str(gremlin_query), code=response.status_code,
                                 record_count=str(len(response.json())) if response.status_code == 200 else '0'))

    @task(33)
    def filter_by_month(self):
        """Query data based on given month."""
        random_months = random.sample(months, k=QUERY_NO_OF_MONTH)
        month = ', '.join(map(str, random_months))

        query = "g.V().has('ecosystem','OPENSHIFT').has('probable_cve', true)" \
                ".has('updated_yearmonth', within({month})).as('event').select('event')" \
                ".local(properties().group().by(key()).by(value()))"\
            .format(month=month)
        gremlin_query = {"gremlin": query}

        self._client_call(gremlin_query, 'filter_by_month')

    @task(33)
    def filter_by_date(self):
        """Query data by given dates."""
        random_dates = random.sample(dates, k=QUERY_NO_OF_DATE)
        date = ', '.join(map(str, random_dates))

        query = "g.V().has('ecosystem','OPENSHIFT').has('probable_cve', true)" \
                ".has('updated_date', within({date})).as('event').select('event')" \
                ".local(properties().group().by(key()).by(value()))"\
            .format(date=date)
        gremlin_query = {"gremlin": query}

        self._client_call(gremlin_query, 'filter_by_date')

    @task(33)
    def filter_by_reponames(self):
        """Query data based on given repo-names."""
        random_reponames = random.sample(repo_names, k=QUERY_NO_OF_REPO)
        repo_name = ', '.join("'{item}'".format(item=str(x)) for x in random_reponames)

        query = "g.V().has('ecosystem','OPENSHIFT').has('probable_cve', true)" \
                ".has('repo_name', within({repo_name})).as('event').select('event')" \
                ".local(properties().group().by(key()).by(value()))"\
            .format(repo_name=repo_name)
        gremlin_query = {"gremlin": query}

        self._client_call(gremlin_query, 'filter_by_reponames')


class QueryIngestedDataTest(HttpLocust):
    """Locust test class."""

    task_set = QueryIngestedDataFequentlyUsedSteps
    host = HOST_URL
    wait_time = between(1, 30)

    def __init__(self):
        """Init method for test class."""
        super(QueryIngestedDataTest, self).__init__()
