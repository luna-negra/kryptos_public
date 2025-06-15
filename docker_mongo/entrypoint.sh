#!/bin/bash

# define variables
MONGO_CMD="mongosh"
MONGO_INIT_KRYPTOS_DBNAME="THIS_IS_SECRET"
MONGO_INIT_KRYPTOS_USERNAME="THIS_IS_SECRET"
MONGO_INIT_KRYPTOS_PASSWORD="THIS_IS_SECRET"

# echo
echo "[KRYPTOS MONGO DB ]"

# run container
echo "start running container for MongoDB version ${MONGO_VERSION}"

# version check
# Choose the correct Mongo shell command based on version
if [[ "$MONGO_VERSION" == "4."* ]]; then
  MONGO_CMD="mongo"
fi

# create new database and user for Kryptos
echo "create new database and user for Kryptos"
${MONGO_CMD} --eval "db.getSiblingDB('${MONGO_INIT_KRYPTOS_DBNAME}').createUser({
  user: '${MONGO_INIT_KRYPTOS_USERNAME}',
  pwd: '${MONGO_INIT_KRYPTOS_PASSWORD}',
  roles: [{ role: 'readWrite', db: '${MONGO_INIT_KRYPTOS_DBNAME}' }]
});"
echo "complete creating new database and user for Kryptos"

# remove root user in Database
echo "remove all root user in this container"
${MONGO_CMD} --eval "db.getSiblingDB('admin').system.users.find({'roles.role': 'root'}).forEach(function(user) {
  db.getSiblingDB('admin').dropUser(user.user);
});"
echo "complete remove all root user in this container"

# complete initdb
echo "complete initdb for Kryptos. Welcome to Kryptos!"

# mongo container will run its daemon automatically.