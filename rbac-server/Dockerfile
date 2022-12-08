FROM python:3.8
# Install libraries
RUN apt-get update && apt-get install -y wget fuse3 libfuse3-3 gnupg2 python3

# Add key
RUN wget -O - http://ppa.moosefs.com/moosefs.key 2>/dev/null | apt-key add - 2>/dev/null
RUN echo "deb http://ppa.moosefs.com/3.0.115/apt/debian/buster buster main" > /etc/apt/sources.list.d/moosefs.list

# Install MooseFS client and cli
RUN apt-get update && apt-get install -y moosefs-client moosefs-cli

WORKDIR /code
COPY requirements.txt /code/
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/
RUN chmod +x /code/entrypoint.sh; mkdir -p /mnt/moosefs
ENTRYPOINT /code/entrypoint.sh

