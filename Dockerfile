FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt pyproject.toml ./
COPY src ./src
COPY data ./data
COPY sql ./sql
COPY reports ./reports
COPY dashboard ./dashboard

RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir -e .
CMD ["python", "-m", "tube_analytics.pipeline"]
