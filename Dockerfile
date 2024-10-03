# Dockerfile

# Step 1: Use the official Python image from Docker Hub
FROM python:3.12-slim

# Step 2: Set environment variables
#ENV PYTHONDONTWRITEBYTECODE=1  # Prevents Python from writing pyc files to disc
#ENV PYTHONUNBUFFERED=1         # Ensures output from Python is sent straight to the terminal

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Copy the requirements file (if you have one) into the container
COPY requirements.txt /app/

# Step 5: Install dependencies from requirements.txt
RUN pip install -r ./requirements.txt

# Step 6: Copy the current directory (your Django project) to /app
COPY . /app/

# Step 7: Expose port 8000 (default port for Django)
EXPOSE 8000

# Step 8: Run the Django development server when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
