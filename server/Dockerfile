FROM ubuntu:jammy

# Replace 1000 with your user / group id
ARG uid=1000
ARG gid=1000
ARG user=user

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt update && \
    apt upgrade -y && \
    apt install -y tzdata sudo net-tools binutils file git vim \
    telnet netcat wget curl lsof \
    iputils-ping iproute2 ethtool traceroute && \
    apt install -y python3 python3-pip && \
    pip3 install grpcio grpcio-tools

RUN groupadd -g ${uid} ${user} && \
    useradd -u ${gid} -g ${user} -G sudo -r ${user} -s /bin/bash && \
    echo 'Defaults visiblepw' >> /etc/sudoers && \
    echo ${user} ' ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    mkdir /home/${user} && \
    chown ${uid}:${gid} -R /home/${user}

WORKDIR /home/${user}

COPY server.py /home/${user}/
COPY api_pb2.py /home/${user}/
COPY api_pb2_grpc.py /home/${user}/
COPY server.crt /home/${user}/
COPY server.key /home/${user}/

USER root
RUN chown ${user}:${user} /home/${user}/server.key && chmod 600 /home/${user}/server.key

USER ${user}

CMD ["python3", "server.py"]
