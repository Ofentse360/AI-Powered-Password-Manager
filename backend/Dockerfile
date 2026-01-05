# backend/Dockerfile

# 1. Use an official Python runtime as a parent image
FROM python:3.10-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Install system dependencies (needed for Postgres driver)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements file first (for better caching)
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application code
COPY . .

# 7. Expose the port FastAPI runs on
EXPOSE 8000

# 8. Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]