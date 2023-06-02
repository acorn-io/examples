# Aiven Redis service Acorn

This Acorn provides a Redis database from the Aiven platform.

## Prerequisites

To use this Acorn, you will need to first create a secret:

```acorn
secrets: "aiven-account"
    type: "opaque"
    data: {
        token: ""
        project: ""
        email: ""
    }
```

```bash
acorn secret create aiven-account --data token=... --data project=... --data email=...
```

## Usage

```bash
Volumes:   <none>
Secrets:   aiven-account, redis-password
Containers: <none>
Ports:     <none>

      --db-name string   Name of the redis service to create. (Default is "[ACORN-NAME]-redis-0")
      --plan string      Plan of the redis service to create. (Default is "free-1")
```
