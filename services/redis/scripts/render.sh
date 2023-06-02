#!/bin/sh

set -eo pipefail
set -x

# Set your Aiven credentials and parameters
EMAIL="${EMAIL}"
PASSWORD="${TOKEN}"
PROJECT="${PROJECT}"
SERVICE_NAME="${REDIS_DB_NAME}"
PLAN="${REDIS_PLAN}"

# Function to create a Redis database
create_redis() {
    echo "Creating Redis database..."
    avn --auth-token "${PASSWORD}" service create $SERVICE_NAME --project $PROJECT -t redis -p $PLAN --cloud aws-us-east-2
    echo "Redis database created successfully."
}

# Function to update a Redis database
update_redis() {
    echo "Updating Redis database..."
    avn --auth-token "${PASSWORD}" service update $SERVICE_NAME --project $PROJECT -p $PLAN
    echo "Redis database updated successfully."
}

# Function to get Redis connection details
create_redis_acorn_service() {
    echo "Getting Redis connection details..."
    avn --auth-token "${PASSWORD}" service get $SERVICE_NAME --project $PROJECT --json > redis_details.json

    address=$(jq -r '.components[0].host' redis_details.json)
    port=$(jq -r '.components[0].port' redis_details.json)
    password=$(jq -r '.connection_info.redis_password' redis_details.json)

    echo "Creating Acorn service..."
cat > /run/secrets/output<<EOF
services: "redis-cloud-server": {
    address: "${address}"
    ports: "6379:${port}"
    secrets: ["redis-password"]
    data: {
        "tls": "required"
    }
}
secrets: "redis-password": {
    type: "token"
    data: token: "${password}"
}
EOF
}


# Function to delete a Redis database
delete_redis() {
    echo "Deleting Redis database..."
    avn --auth-token "${PASSWORD}" service terminate --force --project $PROJECT $SERVICE_NAME
    echo "Redis database deleted successfully."
}

# Main script
if [ "${ACORN_EVENT}" = "create" ]; then
    create_redis
    create_redis_acorn_service
elif [ "${ACORN_EVENT}" = "update" ]; then
    update_redis
    create_redis_acorn_service
elif [ "${ACORN_EVENT}" = "delete" ]; then
    delete_redis
else
    echo "Invalid argument. Please use 'create' or 'delete'."
fi
