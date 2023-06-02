# Writing CRDs

## Overview

This Acorn deploys a k3s HelmChart custom resource to deploy a chart. The Custom Resource is encapsulated in a service Acorn.

## Notes

This Acorn requires elevated Kubernetes permissions to deploy the HelmChart custom resource. It will prompt the user to allow for the requested permissions.

## Prerequisites

This Acorn will only work on k3s cluster running the Acorn runtime.

## Usage

```bash
Volumes:   <none>
Secrets:   redis-password, redis-auth
Containers: <none>
Ports:     <none>

      --repo-url string   The URL of the redis helm chart
```

## Examples

```acorn
acorns: "echo-app": {
    image: "index.docker.io/cloudnautique/echo-app:services"
    links: ["service-redis.redis:redis"]
    publish: "app:5000/http"
    publishMode: "defined"
    secrets: ["service-redis.redis-password:redis-password"]
}

services: "service-redis": {
    build: {
        context: "."
    }
}
```
