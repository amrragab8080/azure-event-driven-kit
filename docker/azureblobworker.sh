#!/bin/bash -xe

export AZURE_CONFIG_DIR=$PWD/.azure
export AZURE_STORAGE_ACCOUNT=$1
export AZURE_STORAGE_KEY=$2
export JOBDIR=$3
export SCRATCHDIR=/scratch
#######################################
env
#######################################
function finish(){
    echo "JOB FINISHED, COMPRESSING OUTPUT..."
    cp $AZ_BATCH_TASK_DIR/*.txt $JOBPATH
    tar -czvf $JOBPATH/../batch_output_$1-logs.tar.gz $JOBPATH/*.txt
    tar -czvf $JOBPATH/../batch_output_$1.tar.gz $JOBPATH/*

    az storage blob upload --container-name $2 --file $JOBPATH/../batch_output_$1-logs.tar.gz --name batchoutput_$1-logs.tar.gz
    az storage blob upload --container-name $2 --file $JOBPATH/../batch_output_$1.tar.gz --name batchoutput_$1.tar.gz

    echo "CLEANUP..."
    rm -rf $JOBPATH
    echo "BATCH JOB DONE"
}

echo "DOWNLOADING INPUT FILES..."
cd $SCRATCHDIR
mkdir -p $PWD/$JOBDIR
export JOBPATH=$PWD/$JOBDIR

az storage blob download --container-name $4 --name $5 --file $JOBPATH/input.zip --output json

unzip $JOBPATH/input.zip -d $JOBPATH
echo "STARTING UP WORKFLOW..."
cd $JOBPATH/

NUMCORES=`expr $(nproc) \/ 2`

trap "finish $3 $6" EXIT

<command>
