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
RUN sudo -u pydor mkdir -vp src
COPY --chown=pydor:pydor . src

WORKDIR /home/pydor/src

RUN sudo -u pydor pip3 install --system --upgrade -r requirements-dev.txt
RUN sudo -u pydor pip3 install --system --upgrade -e .

RUN rm -rf /home/pydor/.cache/pip

USER pydor:pydor

RUN echo "PS1='pydor@docker:\W\$ '" >>/home/pydor/.bashrc

RUN echo 'alias vim=vim.tiny' >>/home/pydor/.bashrc
RUN printf 'syntax on\nset bg=dark\ncolorscheme desert\n' >/home/pydor/.vimrc

RUN git config --global alias.st status
RUN git config --global alias.ci commit

RUN pip3 list

CMD exec /bin/bash -l
