FROM registry.access.redhat.com/ubi8/ubi-minimal

LABEL name="osa api server" \
      description="Probable Vulnerability API server" \
      email-ids="arajkuma@redhat.com" \
      git-url="https://github.com/kubesecurity/osa-api-server" \
      git-path="/" \
      target-file="Dockerfile" \
      app-license="GPL-3.0"


ADD ./requirements.txt /app/
ADD main.py /app/
COPY src/ /app/src/

RUN microdnf install python3 && pip3 install --upgrade pip &&\
    pip3 install -r /app/requirements.txt && rm /app/requirements.txt

ADD scripts/entrypoint.sh /bin/entrypoint.sh

RUN chmod +x /bin/entrypoint.sh

ENTRYPOINT ["/bin/entrypoint.sh"]
