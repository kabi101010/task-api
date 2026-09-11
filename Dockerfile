# Use a small, official Python base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency file first (Docker caches this layer if requirements don't change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Document which port the app listens on
EXPOSE 5000

# Basic healthcheck — Kubernetes/monitoring will build on this concept later
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["python", "app.py"]
