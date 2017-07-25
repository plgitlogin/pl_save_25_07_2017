FROM debian:jessie

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
	sudo \
	locales \
	wget \
	build-essential \
	libssl-dev \
	openssl

#Installing python 3.5.1 from source
RUN wget --no-check-certificate https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tgz \
		-O /tmp/python.tgz &&\
		mkdir -p /tmp/python &&\
		tar xvfz /tmp/python.tgz -C /tmp/python &&\
		cd /tmp/python/Python-3.5.1 &&\
		sh ./configure &&\
		make &&\
		make install

RUN wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py
RUN python3 /tmp/get-pip.py
RUN pip install jinja2
RUN pip install doctest

# Adding sftp lib folder to pythonpath
ENV PYTHONPATH /var/lib/upem:$PYTHONPATH

ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8 
ENV LC_TYPE en_US.UTF-8
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
RUN locale-gen "en_US.UTF-8" &&\
		dpkg-reconfigure locales

ADD execute_in_environment.sh /usr/bin/execute_in_environment
ADD run_code2.py /usr/bin/run_code
RUN chmod +x /usr/bin/execute_in_environment
