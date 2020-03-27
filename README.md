# API Server

![build and test](https://github.com/fabric8-analytics/osa-api-server/workflows/build%20and%20test/badge.svg)

## Development

Make sure you have `Python >= 3.6` installed in your development environment,

Install `virtualenv`, activate it and then install project dependencies

```
pip install -r requirements.txt
```

Run API server,
```
gunicorn --pythonpath . -k sync -b localhost:5000 main:app --reload
```

Swagger/OpenAPI based documentation can be obtained by accessing the following URL,

[http://localhost:5000/api/swagger](http://localhost:5000/api/swagger)

Run unittest,
```
pip install -r requirements-test.txt
pytest
```

### To Deploy it on OpenShift,

- Build container image (e.g. docker)
- Push container image to registry (e.g. quay.io)
- use `oc` to deploy it on OpenShift,
```
docker build --no-cache -t <image_name:tag> .
docker push <registry>/<image_name:tag>
oc process -f openshift/template.yaml -p DOCKER_REGISTRY=<registry> -p DOCKER_IMAGE=<image_name> -p GREMLIN_DEFAULT_HOST=<gremlin_host> -p GREMLIN_DEFAULT_PORT=<gremlin_port> | oc create -f -
```

## Ingest historical data

A [command tool](tools/ingest_historical_csv.py) has been created to ingest historical data into database through API server,

Make sure dependencies of [command tool](tools/ingest_historical_csv.py) has been installed in your development `virtualenv`,

```
pip install -r tools/requirements.txt
```

#### To ingest CSV to DB,

```
python tools/ingest_historical_csv.py <path_to_csv_file> --insert
```

#### To ingest Feedback,
```
python tools/ingest_historical_csv.py <path_to_csv_file> --feedback
```

## QA Script Usage

A [documentation](qa/README.md) has been created with details on how we can use QA scripts. 
