FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y \
      python3-rich \
      python3-apt \
      python3-click
ADD assets/15update-stamp /etc/apt/apt.conf.d/15-update-stamp
RUN mkdir -p /usr/src/apt-ostree
WORKDIR /usr/src/apt-ostree
