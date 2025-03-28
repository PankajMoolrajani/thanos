FROM ubuntu:latest



# Update package lists and install basic utilities
RUN apt-get update && \
    apt-get install -y \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*


# Set working directory
WORKDIR /app
# Copy application files
COPY . /app/



# Default command
CMD ["/bin/sleep", "21600"]
