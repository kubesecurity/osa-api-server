FROM registry.centos.org/centos/centos:7

LABEL name="osa api server" \
      description="Probable Vulnerability API server" \
      email-ids="arajkuma@redhat.com" \
      git-url="https://github.com/fabric8-analytics/osa-api-server" \
      git-path="/" \
      target-file="Dockerfile" \
      app-license="GPL-3.0"

RUN yum install -y epel-release &&\
    yum install -y git python36-pip python36-devel &&\
    yum clean all

COPY ./requirements.txt /

RUN pip3 install --upgrade pip &&\
    pip3 install -r requirements.txt && rm requirements.txt

ADD main.py /app/
COPY src/ /app/src/

ADD scripts/entrypoint.sh /bin/entrypoint.sh

RUN chmod +x /bin/entrypoint.sh

ENTRYPOINT ["/bin/entrypoint.sh"]
