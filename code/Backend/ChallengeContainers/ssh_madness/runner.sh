#!/bin/bash
del_deny() {
    sleep 120
    sed -i "/DenyUsers root@$1/d" /etc/ssh/sshd_config
    service ssh restart
}

sleep 10

TARGET=$(last | grep "still logged in" | awk "{printf \"/dev/%s,%s\n\", \$2, \$3}")
if test -z "$TARGET"; then exit 0; fi
for line in $TARGET; do
    IFS="," read -r dev ip <<< $line
    bash -c "echo -e \"\nDetected Unauthorized Access from IP: $ip\" > $dev"
done


sleep 20
TARGET_SEC=$(last | grep "still logged in" | awk "{printf \"/dev/%s,%s\n\", \$2, \$3}")
if test -z "$TARGET_SEC"; then exit 0; fi
while IFS="," read -r dev ip; do 
    if grep -q "$ip" <<< "$TARGET"; then
        echo -e "\nUPDATING FIREWALL TO BLOCK $ip" > $dev
        proc=$(ps -aux | ps -aux | grep --color=never -E 'sshd: [[:alnum:]]+@' | grep --color=never "$(basename $dev)" | awk '{print $2}')
        DENY_TEXT="DenyUsers root@$ip"

        # Funny
        # head -n 20 /dev/urandom > $dev
        echo -e "\nYOU ARE BLOCKED!\n\n" > $dev
        sleep 2
        kill $proc

        # Deny future login attempts
        echo $DENY_TEXT >> /etc/ssh/sshd_config
        service ssh restart

        # Fork process to delete text in the future
        (del_deny $ip) &
    fi
done <<< "$TARGET_SEC"