FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (Docker caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY . .

# Default command
CMD ["python", "run.py", "--test"]