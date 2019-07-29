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
	git less vim-tiny unzip bash-completion make

RUN apt-get clean
RUN apt-get autoremove -y --purge

RUN rm -rf /var/lib/apt/lists/*
RUN rm -f /var/cache/apt/archives/*.deb
RUN rm -f /var/cache/apt/*cache.bin

RUN printf 'pydor\tALL=NOPASSWD: ALL\n' >/etc/sudoers.d/pydor
RUN chmod 440 /etc/sudoers.d/pydor

ARG PYDOR_UID=1000
ARG PYDOR_GID=1000

RUN groupadd -g ${PYDOR_GID} pydor
RUN useradd -c pydor -m -d /home/pydor -s /bin/bash -G staff -g ${PYDOR_GID} -u ${PYDOR_UID} pydor

RUN chgrp -v staff /usr/local/bin
RUN chmod -v g+ws /usr/local/bin

WORKDIR /home/pydor

RUN sudo -u pydor mkdir -vp src/docs

COPY --chown=pydor:pydor requirements-dev.txt src
RUN sudo -u pydor pip3 install --system --upgrade -r src/requirements-dev.txt

COPY --chown=pydor:pydor docs/requirements.txt src/docs
RUN sudo -u pydor pip3 install --system --upgrade -r src/docs/requirements.txt

COPY --chown=pydor:pydor requirements.txt src
RUN sudo -u pydor pip3 install --system --upgrade -r src/requirements.txt

RUN rm -rf .cache/pip

USER pydor:pydor
WORKDIR /home/pydor

RUN git config --global alias.st status
RUN git config --global alias.ci commit

RUN echo "PS1='pydor@docker:\W\$ '" >>.bashrc

RUN echo 'umask 0027' >>.bashrc
RUN echo 'alias vim=vim.tiny' >>.bashrc

USER root:root
WORKDIR /home/pydor

COPY --chown=pydor:pydor setup.cfg setup.py pydor.py src/
RUN (cd src && sudo -u pydor pip3 install --system --upgrade -e .)

USER pydor:pydor
WORKDIR /home/pydor/src

CMD exec /bin/bash -l
