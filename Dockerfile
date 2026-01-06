# We use the exact version you are comfortable with
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required for building some AI libraries
# (Python 3.12 sometimes needs these for c++ extensions in libraries like Chroma/LangChain)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]