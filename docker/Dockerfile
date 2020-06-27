FROM nvidia/cuda:latest
RUN apt update && apt install build-essential unzip pigz pv wget curl python3-pip -y && apt clean

RUN pip3 install azure-cli
RUN wget https://aka.ms/downloadazcopy-v10-linux && \
    tar -xvf downloadazcopy* && \
    mv azcopy*/azcopy /usr/bin
    
ADD azureblobworker.sh /opt/azureblobworker.sh
RUN chmod +x /opt/azureblobworker.sh
