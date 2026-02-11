# Dockerfile for LPMD Runner Service
FROM python:3.10-slim

WORKDIR /app

# Copy the project files
COPY . /app

# Install dependencies
RUN pip install flask gunicorn

# Install project dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.web.lpmd_runner:app"]