# Prepare base image
FROM mongo:latest

# Create directory for the init script and copy it
COPY entrypoint.sh /docker-entrypoint-initdb.d/entrypoint.sh
RUN chmod 755 /docker-entrypoint-initdb.d/entrypoint.sh

# Expose port
EXPOSE 27017

# command executing mongod with binding all ip is innated in mongo image.
# if you need to change it, please add CMD command below with --auth option
CMD ["mongod", "--auth"]

# Please Note
# run the container with --auth option.
# if you have any trouble with 'WARNING: MongoDB 5.0+ requires a CPU with AVX support, and your current system does not appear to have that!'
# you have to use mongodb image with tag '4'
# FROM mongo:4
