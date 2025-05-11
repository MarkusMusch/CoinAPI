# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the rest of the application code into the container
COPY . .

# Install the dependencies
RUN poetry install --no-root

# Ensure the backend and frontend directories are in the Python path
ENV PYTHONPATH=/app

# Copy the prefilled SQLite database into the container
COPY . /funding_history.db

# Expose the port the app runs on
EXPOSE 8050

# Command to run the application
CMD ["poetry", "run", "python", "frontend/app.py"]