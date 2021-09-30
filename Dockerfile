FROM ubuntu:latest

RUN apt-get update && \
	apt-get install -y curl python3.8 python3.8-distutils && \
	ln -s /usr/bin/python3.8 /usr/bin/python && \
	rm -rf /var/lib/apt/lists/*

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py && \
    python -m pip install -U pip==20.3.3

COPY . .

RUN pip install -r requirements.txt

CMD python main.py