FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y \
      git \
      python3-pip \
      python3-pbr \
      python3-rich \
      python3-apt \
      python3-click \
      debos \
      mmdebstrap \
      binfmt-support \
      btrfs-progs \
      busybox \
      bzip2 \
      ca-certificates \
      dosfstools \
      e2fsprogs \
      equivs \
      fdisk \
      f2fs-tools \
      git \
      gzip \
      pigz \
      libostree-1-1 \
      libslirp-helper \
      linux-image-amd64 \
      ostree \
      openssh-client \
      parted \
      pkg-config \
      qemu-system-x86 \
      qemu-user-static \
      qemu-utils \
      rsync \
      systemd \
      systemd-container \
      unzip \
      user-mode-linux \
      xfsprogs \
      xz-utils \
      zip
ADD assets/15update-stamp /etc/apt/apt.conf.d/15-update-stamp
RUN mkdir -p /usr/src/apt-ostree
WORKDIR /usr/src/apt-ostree
