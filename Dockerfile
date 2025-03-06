#use an official Python runtime as a parent image
FROM python:3.10

#set the working directory in the container 
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install system dependencies (for leafmap and geospatial libraries)
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Install required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8501 for Streamlit
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "sampling_regions.py", "--server.port=8501", "--server.address=0.0.0.0"]
