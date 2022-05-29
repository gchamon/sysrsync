#!/usr/bin/env bash
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

cd $SCRIPT_DIR/..

set -euo pipefail

echo starting ssh server...
docker-compose up --detach openssh-server

echo running tests
docker-compose up --exit-code-from sysrsync-client sysrsync-client

docker-compose down
