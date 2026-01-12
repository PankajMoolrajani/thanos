FROM ubuntu:latest

# Update package lists and install basic utilities
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app/

# Install Python dependencies
RUN pip3 install -r src/requirements.txt --break-system-packages

# Expose Streamlit port
EXPOSE 8501

# Default command - run Streamlit app
CMD ["streamlit", "run", "src/streamlit_app/app.py", "--server.address", "0.0.0.0"]
