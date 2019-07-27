FROM debian:buster-slim

LABEL maintainer="Jeremías Casteglione <jrmsdev@gmail.com>"
LABEL version="19.7.27"

USER root:root
WORKDIR /root

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get clean
RUN apt-get update

RUN apt-get dist-upgrade -y --purge
RUN apt-get install -y --no-install-recommends sudo python3 python3-pip \
	git less vim-tiny

RUN apt-get clean
RUN apt-get autoremove -y --purge

RUN rm -rf /var/lib/apt/lists/*
RUN rm -f /var/cache/apt/archives/*.deb
RUN rm -f /var/cache/apt/*cache.bin

COPY docker/sudoers /etc/sudoers.d/pydor
RUN chmod 440 /etc/sudoers.d/pydor

ARG PYDOR_UID=1000
ARG PYDOR_GID=1000

RUN groupadd -g ${PYDOR_GID} pydor
RUN useradd -c pydor -m -d /home/pydor -s /bin/bash -g ${PYDOR_GID} -u ${PYDOR_UID} pydor

USER pydor:pydor
WORKDIR /home/pydor

COPY --chown=pydor:pydor .ci/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-warn-script-location -r /tmp/requirements.txt

RUN rm -rf .cache/pip
RUN rm -f /tmp/requirements.txt

RUN echo "PS1='pydor@docker:\W\$ '" >>.bashrc

RUN git config --global alias.st status
RUN git config --global alias.ci commit

RUN mkdir -vp src
WORKDIR /home/pydor/src

CMD /bin/bash -i -l
