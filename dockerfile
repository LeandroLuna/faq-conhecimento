# Build: docker build -t faq-conhecimento .

# Use an official Python runtime as a parent image
FROM python:3.9.19

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run index.py when the container launches
CMD ["streamlit", "run", "index.py"]

# Execute: docker run -it --rm -p 8501:8501 faq-conhecimento