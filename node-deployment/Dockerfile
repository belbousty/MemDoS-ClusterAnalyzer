# Dockerfile for kind-node with a simple patch enabling to launch cri-rm

# Base image (xUbuntu 20.04)
FROM quay.io/aojea/kindnode:crio1630331170

COPY sources.list /etc/apt/

# installing perf binary
RUN echo Y | apt update || true 
RUN echo Y | apt upgrade || true 
RUN echo Y | apt install linux-tools-generic
RUN cp /usr/lib/linux-tools-5.11.0-49/perf /root

RUN echo "Installing CRI-RM Packages ..." \
  && curl -sLO https://github.com/intel/cri-resource-manager/releases/download/v0.8.3/cri-resource-manager_0.8.3_ubuntu-20.04_amd64.deb && dpkg -i cri-resource-manager_0.8.3_ubuntu-20.04_amd64.deb 

RUN echo "Copying required config file : policy + logs rules"

COPY ./fallback.cfg /etc/cri-resmgr/fallback.cfg

RUN echo "Manage systemctl services" \
 && systemctl enable containerd \
# && systemctl disable crio \
 && systemctl enable cri-resource-manager \
 && sed '/KUBELET_EXTRA_ARGS/ s!$! --container-runtime-endpoint=/var/run/cri-resmgr/cri-resmgr.sock!' -i /etc/default/kubelet \
 && systemctl enable kubelet.service