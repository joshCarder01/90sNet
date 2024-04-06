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
RUN service ssh start
RUN echo "Welcome" > hello_world.txt
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]