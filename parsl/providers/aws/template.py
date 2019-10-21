import os

# this exists test is necessary so that we can import the
# AWS provider even when this file does not exist.
if os.path.exists("rsync-callback-ssh"):
    with open("rsync-callback-ssh","r") as f:
        private_key = f.read()
else:
    private_key = ""

template_string = """#!/bin/bash
cd ~
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y python3 python3-pip libffi-dev g++ libssl-dev git rsync
pip3 install numpy scipy pytest==4.0.2
pip3 install git+https://github.com/benclifford/parsl@tmp

mkdir .ssh
chmod go-rwx .ssh

cat > .ssh/id_rsa <<EOF
{private_key}
EOF

# ideally a known hosts file would be transmitted here
# but that is a bit more config awkwardness - the full user
# known hosts on my submit environment was too big to
# fit into AWS userdata, which this template must fit into.
cat > .ssh/config <<EOF
Host *
    StrictHostKeyChecking no
EOF

chmod go-rwx .ssh/id_rsa
chmod go-rwx .ssh/config


# Many of these really could go in worker_init rather than in
# the AWS template. Including the parsl install, tbh - if it installs
# the wrong version by default (which it often will) then it probably
# shouldn't be there.



$worker_init

$user_script

# Shutdown the instance as soon as the worker scripts exits
# or times out to avoid EC2 costs.
if ! $linger
then
    halt
fi
""".format(private_key=private_key)
