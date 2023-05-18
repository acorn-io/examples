#!/bin/bash

set -eo pipefail

if [ "$ACORN_EVENT" = "delete" ]; then
    gomplate -f /acorn/manifests/chart.tmpl | kubectl delete -f -
    exit 0
fi

gomplate -f /acorn/manifests/chart.tmpl | kubectl apply -f -
password=$(</acorn/secrets/token)



cat > /run/secrets/output<<EOF
services: redis: {
    address: "redis-master.${ACORN_NAMESPACE}.svc.cluster.local"
    ports: "6379"
    secrets: ["redis-auth"]
}
secrets: "redis-auth": {
    type: "opaque"
    data: token: "${password}"
}
EOF