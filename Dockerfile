FROM python:3.5

LABEL maintainer "Costin Bleotu <costin.bleotu@databus.systems>

RUN pip install --no-cache-dir --upgrade \
	pip \
	setuptools


ADD requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --use-wheel --no-index --find-links=wheeldir \
    -r requirements.txt
ADD run_ssh.py /usr/bin/

ENTRYPOINT ["python3", "/usr/bin/run_ssh.py"]

