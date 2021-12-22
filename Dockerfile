FROM python:3.8

WORKDIR /app

# Setup virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source
COPY . .

# Expose port
EXPOSE 5000

# Set env variables
ENV FLASK_APP=run.py
ENV FLASK_DEBUG=1

# Run application
CMD ["flask", "run", "--host=0.0.0.0"]
