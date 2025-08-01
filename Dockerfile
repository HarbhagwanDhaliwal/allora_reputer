# Use the Python base image
FROM amd64/python:3.9-buster

# Install necessary build tools and Go
RUN apt-get update \
    && apt-get install -y curl wget git make build-essential python3-dev \
    && rm -rf /usr/local/go \
    && curl -L https://go.dev/dl/go1.22.4.linux-amd64.tar.gz | tar -xzf - -C /usr/local \
    && echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> $HOME/.bash_profile \
    && echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> $HOME/.bash_profile \
    && . $HOME/.bash_profile \
    && go version

# Set Go environment variables directly for Docker (without relying on bash profile)
ENV GOROOT=/usr/local/go
ENV GOPATH=/go
ENV PATH=$PATH:$GOROOT/bin:$GOPATH/bin

# Create the directory for the Go project and clone the repository
WORKDIR /app
RUN git clone https://github.com/allora-network/allora-chain.git

# Navigate into the Go project and run `make install`
WORKDIR /app/allora-chain
RUN make install

# Copy only the requirements.txt file first
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt  # Explicitly provide full path to requirements.txt

# Now copy the rest of the application files
COPY . /app

# Expose the necessary ports
EXPOSE 8000

# Set environment variables
ENV NAME sample

# Run gunicorn when the container launches and bind port 8000 from app.py
CMD ["gunicorn", "-b", ":8099", "app:app"]