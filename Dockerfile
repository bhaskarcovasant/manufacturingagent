FROM python:3.12-slim


WORKDIR /app

# Copy requirements first for better caching
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Command to run the deploy service
CMD ["adk", "web"]
