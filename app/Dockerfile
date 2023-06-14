FROM python:3.9.3-slim

# Set working dir
WORKDIR /app

# Copy application code
COPY . .

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Run the application
# Set the command to run your application
CMD gunicorn --bind 0.0.0.0:5000 index:app
