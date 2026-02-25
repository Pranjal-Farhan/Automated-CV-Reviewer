# ──────────────────────────────────────────────
# Stage 1: Use official Python as the base image
# ──────────────────────────────────────────────
FROM python:3.11-slim

# Prevent Python from writing .pyc files & enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# ──────────────────────────────────────────────
# Stage 2: Install dependencies first (cached layer)
# ──────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ──────────────────────────────────────────────
# Stage 3: Copy the application source code
# ──────────────────────────────────────────────
COPY . .

# ──────────────────────────────────────────────
# Stage 4: Define the default command
# ──────────────────────────────────────────────
# ENTRYPOINT makes "run.py" the fixed command;
# users pass the PDF filename as an argument
ENTRYPOINT ["python", "run.py"]