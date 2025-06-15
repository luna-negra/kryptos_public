# Prepare base image
FROM python:3.12-slim

# Copy scripts to container
COPY kryptos_bot/ /usr/local/src/kryptos_bot

# Move to /kryptos
WORKDIR /usr/local/src/kryptos_bot

# Change permission of entrypoint.sh
# Install pip packages and create normal user
RUN chmod 755 ./entrypoint.sh && pip install -r ./requirements.txt

# Run scripts entrypoint.sh to check prerequisites
ENTRYPOINT ["./entrypoint.sh"]

# Run Command
CMD ["python", "execute.py"]