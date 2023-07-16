import pathlib

# default workspace
WORKSPACE = pathlib.Path("/var/tmp/apt-ostree")
OSTREE_PATH = pathlib.Path("/ostree")

# support debian verisons
SUITES = ["bookworm", "trixie"]

# ADDITIONAL_PACKAGES
PACKAGES = [
    "ca-certificates",
    "bash",
    "bash-completion",
    "bzip2",
    "file",
    "gnupg",
    "less",
    "lzma",
    "mawk",
    "whiptail",
    "lsb-release",
    "sudo",
    "parted",
    "vim",
    "iproute2",
    "iputils-ping",
    "locales",
    "netbase",
    "net-tools",
    "openssh-client",
    "openssh-server",
    "procps",
    "dbus",
    "policykit-1",
    "libnss-resolve",
    "dbus-user-session",
    "iptables",
    "nftables",
    "apparmor",
    "curl",
    "wget",
    "git",
    "bubblewrap",
    "python3-apt",
    "python3-rich",
]

ARTIFACT = "rootfs.tar.gz"
