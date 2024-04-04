FROM python:slim AS db_builder

WORKDIR /home
COPY gen_tables.py /home/gen_tables.py

RUN python gen_tables.py


FROM debian:bookworm AS base

WORKDIR /home
RUN set -ex;         \
    apt-get update;  \
    apt-get install -y --no-install-recommends libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && apt-get clean

FROM base AS builder

RUN apt-get update;  \
    apt-get install -y cmake gcc \
    && rm -rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && apt-get clean \
    && mkdir /home/src /home/build

COPY CMakeLists.txt /home
COPY src/simple.c /home/src/simple.c

WORKDIR /home/build

RUN cmake .. && make

FROM base AS runner
ARG port=3333

RUN apt-get update;  \
    apt-get install -y socat \
    && rm -rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && apt-get clean \
    && chmod -R 555 /root

COPY --from=db_builder --chmod=0444 /home/db_authenticator.db /home
COPY --from=builder --chmod=0555 /home/build/SimplePuzzle /home

EXPOSE ${port}

CMD socat TCP-LISTEN:${port},tcpwrap=script,reuseaddr,fork EXEC:'/home/SimplePuzzle',stderr,pty,rawer
#
# Install common executables
#
# FROM ubuntu:20.04 as COMMON

# COPY install_required_packages.sh /root/install_required_packages.sh
# COPY challenge-listener.py /usr/local/bin/challenge-listener.py

# RUN apt update \
#     && /root/install_required_packages.sh \
#     && chmod 755 /usr/local/bin/challenge-listener.py

#
# Challenge Specific
#
# FROM COMMON as CHALLENGE

# RUN useradd -M -d /home/{{challenge.username}} {{challenge.username}}

# WORKDIR /home/{{challenge.username}}/server

# COPY server.zip /home/{{challenge.username}}/server/server.zip
# COPY requires-server /home/{{challenge.username}}/requires-server
# COPY flag.txt /home/{{challenge.username}}/flag.txt

# RUN unzip server.zip &&\
#     chmod -R 755 $(pwd) &&\
#     mv * ..

# WORKDIR /home/{{challenge.username}}
# USER {{challenge.username}}

# CMD {{challenge.listener_command}}
