# Prepare base image
FROM mongo:latest

# Create directory for the init script and copy it
COPY entrypoint.sh /docker-entrypoint-initdb.d/entrypoint.sh
RUN chmod 755 /docker-entrypoint-initdb.d/entrypoint.sh

# Expose port
EXPOSE 27017

# Clean-up after initialization and start MongoDB
CMD mongod & \
    sleep 10 && \
    rm -f /docker-entrypoint-initdb.d/entrypoint.sh && \
    wait $!

# Please Note
# run the container with --auth option.
# if you have any trouble with 'WARNING: MongoDB 5.0+ requires a CPU with AVX support, and your current system does not appear to have that!'
# you have to use mongodb image with tag '4'
# FROM mongo:4