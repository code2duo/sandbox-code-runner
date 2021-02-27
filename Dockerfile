FROM debdutgoswami/ubuntu20.04-with-python3.9:latest

LABEL maintainer="Debdut Goswami - debdutgoswami@gmail.com"

# set working directory
WORKDIR /root/src/app

# copying requirements.txt
# we copy the dependency file first because, docker creates layers at each step
# copying entire project file will end up taking a lot of time and if something goes wrong
# we need to re-build it and it would again take the extra timne of coying of entire project
COPY requirements.txt .
# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copying project files
COPY . .

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "--timeout", "0", "code_runner.wsgi:application"]

# creating a restricted user
RUN groupadd --gid 5000 restricteduser \
    && useradd --home-dir /home/restricteduser --create-home --uid 5000 \
        --gid 5000 --shell /bin/sh --skel /dev/null restricteduser
