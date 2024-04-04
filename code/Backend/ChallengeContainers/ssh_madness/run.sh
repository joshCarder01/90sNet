#!/bin/bash
pushd /usr/local/share 
# Generate Users
./generate_ssh_users.sh
# Remove script evidence
rm -r *
popd

# Now run the ssh server
cd /home
service ssh start -D
#/usr/sbin/sshd -D

wait -n
exit $#

