FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir "pyyaml>=5.4"

# Bind to all interfaces inside the container; the port is mapped to the host.
ENV PLANTMEMORY_HOST=0.0.0.0
EXPOSE 7700

# Serve the hub (no browser inside the container — open http://localhost:7700).
CMD ["python", "-m", "plant_memory", "hub", "--no-open"]
