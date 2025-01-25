# Prepare base image
FROM mongo:latest

# Create directory for the init script and copy it
COPY init_kryptos_mongo.js /docker-entrypoint-initdb.d/init_kryptos_mongo.js
RUN chmod 755 /docker-entrypoint-initdb.d/init_kryptos_mongo.js

# Expose port
EXPOSE 27017

# Clean-up after initialization and start MongoDB
CMD mongod & \
    sleep 10 && \
    rm -f /docker-entrypoint-initdb.d/init_kryptos_mongo.js && \
    wait $!

# Please Note
# run the container with --auth option.
# if you have any trouble with 'WARNING: MongoDB 5.0+ requires a CPU with AVX support, and your current system does not appear to have that!'
# you have to use mongodb image with tag '4'
# FROM mongo:4
