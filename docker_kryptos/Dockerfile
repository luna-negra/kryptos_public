# Prepare base image
FROM python:3.12-slim

# Copy scripts to container
COPY kryptos /usr/local/src/kryptos

# Move to /kryptos
WORKDIR /usr/local/src/kryptos

# Change permission of entrypoint.sh
# Install pip packages
RUN chmod 755 ./entrypoint.sh && \
    pip install -r ./requirements.txt

# Set port
EXPOSE 8000

# Run scripts
ENTRYPOINT ["./entrypoint.sh"]

# All files and folders must be in kryptos folder