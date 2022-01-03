FROM ghcr.io/processone/ejabberd:21.12

COPY ./run.sh ./run.sh

ENTRYPOINT ./run.sh
