FROM python:2.7

WORKDIR /app
COPY requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /app
CMD ["/bin/bash"]
