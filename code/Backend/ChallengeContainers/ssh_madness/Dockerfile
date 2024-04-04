from debian:bookworm

RUN apt-get update \
    && apt-get install --no-install-recommends -y openssh-server openssl \
    && rm -rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && apt-get clean

RUN mkdir /var/run/sshd
RUN echo 'root:toor' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
#RUN service ssh start
RUN echo "Welcome" > /score.txt

# COPY All Build Files
COPY --chmod=0500 generate_ssh_users.sh run.sh /usr/local/share/
COPY --chmod=0400 common_first_names.txt common_last_names.txt common_passwords.txt /usr/local/share/

WORKDIR /home

EXPOSE 22
CMD "/usr/local/share/run.sh"