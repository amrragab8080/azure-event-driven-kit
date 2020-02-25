FROM alzhang/spectrum-master-rstudio:v1.4

RUN apt update && apt install build-essential unzip pigz pv -y && apt clean
RUN pip3 install azure-cli snakemake
ADD azureblobworker.sh /opt/azureblobworker.sh
RUN chmod +x /opt/azureblobworker.sh
