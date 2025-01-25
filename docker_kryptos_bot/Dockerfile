# Prepare base image
FROM python:3.12-slim

# Copy scripts to container
COPY kryptos_bot/ /usr/local/src/kryptos_bot

# Move to /kryptos
WORKDIR /usr/local/src/kryptos_bot

# Change permission of entrypoint.sh
# Install pip packages
RUN chmod 755 ./entrypoint.sh && \
    pip install -r ./requirements.txt

# Run scripts
ENTRYPOINT ["./entrypoint.sh"]

# All files and folders must be in kryptos folder