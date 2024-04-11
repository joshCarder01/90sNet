from debian

RUN apt-get update -y \
    && apt-get install -y \
        openssh-server \
        nmap \
        iproute2 \
        ncat \
    && apt-get clean
RUN mkdir /var/run/sshd
RUN echo 'root:90sNetProxyPass' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

RUN echo 'Baldwin: 10.54.0-60.0-60\nTUC: 10.61.0-60.0-60\nManti: 10.84.0-60.0-60\nOldChem: 10.109.0-60.0-60\nReviechel: 10.22.0-60.0-60\nZimmer: 10.118.0-60.0-60' \
            > /home/subnets.txt && \
            cat /home/subnets.txt > /etc/motd
RUN service ssh start
RUN echo "Welcome" > hello_world.txt
WORKDIR /home
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]