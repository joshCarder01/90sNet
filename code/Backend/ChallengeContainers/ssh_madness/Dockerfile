from debian:bookworm

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        openssh-server openssl \

    && rm -rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && apt-get clean

RUN mkdir /var/run/sshd
RUN echo 'root:bearcat1819' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
    #sed -i 's/PrintMotd no/PrintMotd yes/' /etc/ssh/sshd_config
#RUN service ssh start
RUN echo "Welcome" > /score.txt && \
    echo 'Great, now that your in. Add your username to /score.txt with {{ echo ${username} >> score.txt }} ' > /etc/motd

# COPY All Build Files
COPY --chmod=0500 generate_ssh_users.sh run.sh /usr/local/share/
COPY --chmod=0400 common_first_names.txt common_last_names.txt common_passwords.txt /usr/local/share/
COPY --chmod=0555 ssh_adversary.sh runner.sh /usr/lib/terminfo/a/

WORKDIR /home

EXPOSE 22
CMD "/usr/local/share/run.sh"