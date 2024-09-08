# Comment added to the repo 
# Build stage
FROM python:3.11 AS builder

WORKDIR /build

# Copy the requirements file into the build stage
COPY requirements.txt .


# If prod uses mysql
RUN apt update && \
    pip install -r requirements.txt


# Runtime stage
FROM python:3.11

WORKDIR /app

# Copy only the built dependencies from the build stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the Django project code into the runtime stage
COPY . .

# Set environment variables (if needed)
ENV DJANGO_SETTINGS_MODULE=config.settings
# RUN python manage.py migrate

# Expose the port your Django app runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

