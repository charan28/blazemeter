FROM alpine:3.6

# Install Python3 and Pip
RUN sed -i -e 's/dl-cdn/dl-4/' /etc/apk/repositories && \
    apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    rm -r /root/.cache

# Install pylint
RUN apk add --no-cache --update python3-dev gcc build-base
RUN pip3 install -U pylint

# Set the working directory
WORKDIR /app

# Bundle app source
COPY . /app

# Install required modules
RUN pip3 install -r requirements.txt

# Modify permissions so we can run scripts
RUN chmod -R a+rwx /app

# Add jenkins group
RUN addgroup jenkins

# Add jenkins user
RUN adduser -S -G jenkins jenkins
USER jenkins