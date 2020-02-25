import json
import logging
import uuid
import os
import azure.functions as func
import azure.batch.batch_service_client as batch
import azure.batch.batch_auth as batch_auth
import azure.batch.models as batchmodels

def add_tasks(batch_service_client, pool_id, task_id, docker_image, storage_account, storage_key, container_name, file_name,output_container):
    job_id="batchjob"
    try:
        job = batchmodels.JobAddParameter(
        id=job_id,
        pool_info=batchmodels.PoolInformation(pool_id=pool_id))
        batch_service_client.job.add(job)
        logging.info('Adding job {} to pool...'.format(job_id))
    except Exception:
        logging.info('Job ID: {} already exists and associated with pool...'.format(job_id))
        pass

    logging.info('Adding tasks to job [{}]...'.format(job_id))

    # This is the user who run the command inside the container.
    # An unprivileged one
    user = batchmodels.AutoUserSpecification(
        scope=batchmodels.AutoUserScope.task,
        elevation_level=batchmodels.ElevationLevel.admin
    )

    # This is the docker image we want to run
    task_container_settings = batchmodels.TaskContainerSettings(
        image_name=docker_image,
        container_run_options='--rm -v /scratch:/scratch'
    )
    
    # The container needs this argument to be executed
    task = batchmodels.TaskAddParameter(
        id=task_id,
        command_line='/opt/azureblobworker.sh %s %s %s %s %s %s'%(storage_account,storage_key,task_id,container_name, file_name, output_container),
        container_settings=task_container_settings,
        user_identity=batchmodels.UserIdentity(auto_user=user)
    )
    batch_service_client.task.add(job_id, task)


def main(event: func.EventGridEvent):

    logging.info(os.environ)

    result = json.dumps({
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
    })

    BATCH_ACCOUNT_NAME=os.getenv('BATCH_ACCOUNT_NAME')
    BATCH_ACCOUNT_KEY=os.getenv('BATCH_ACCOUNT_KEY')
    BATCH_ACCOUNT_URL=os.getenv('BATCH_ACCOUNT_URL')
    BATCH_POOL_ID=os.getenv('BATCH_POOL_ID')
    BATCH_DOCKER_IMAGE=os.getenv('BATCH_DOCKER_IMAGE')
    STORAGE_ACCOUNT=os.getenv('STORAGE_ACCOUNT_NAME')
    STORAGE_KEY=os.getenv('STORAGE_KEY')
    OUTPUT_CONTAINER=os.getenv('OUTPUT_CONTAINER')

    credentials = batch_auth.SharedKeyCredentials(BATCH_ACCOUNT_NAME,
                                                  BATCH_ACCOUNT_KEY)

    batch_client = batch.BatchServiceClient(
        credentials,
        batch_url=BATCH_ACCOUNT_URL)

    taskid=str('task-')+str(uuid.uuid4())[:8]

    storage_path=str(event.subject)
    storage_path_split=storage_path.split("/")
    container_name=storage_path_split[4]
    file_name=storage_path_split[6]

    add_tasks(batch_client,BATCH_POOL_ID,taskid,BATCH_DOCKER_IMAGE,STORAGE_ACCOUNT,STORAGE_KEY,container_name,file_name,OUTPUT_CONTAINER)
    logging.info('Task Submitted as task: %s'%taskid)
    logging.info(result)
