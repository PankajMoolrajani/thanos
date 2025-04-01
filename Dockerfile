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
RUN pip3 install -r requirements.txt


# Default command
CMD ["/bin/sleep", "21600"]
