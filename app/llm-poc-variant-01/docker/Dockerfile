FROM --platform="linux/amd64" python:3.10-bookworm

COPY . .

ARG REQUESTS_CA_BUNDLE
ENV REQUESTS_CA_BUNDLE="${REQUESTS_CA_BUNDLE:-}"

RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/bash"]