# Event Driven Batch Deployment Kit
### Using a push to storage event driven model, execute a templated workflow against an application in the Azure Container Registry executed in Azure Batch. For HPC based workflows, tightly coupled MPI based workflows are also supported. 

![Alt text](imgs/arch.png?raw=true "Event Driven Kit Arch")

## Deployment
After git cloning the kit, deploy the `storage-event-batch.json` in Azure Resource Manager filling in the relevant values. The ARM template is set to create if resource doesnt exist. As a tip keep track of the ids of the resources you deploy as you will need them later.

![Alt text](imgs/template.png?raw=true "ARM Template")

Upload the function from `StorageEventBatchFunction` in the Azure Function created in the ARM deployment
Deploy your docker image into the Azure Container Registry

## Execution
The EventGrid subscription operates on a filtered message uploading a *.zip file. The compressed archive will be extracted on the execute node. The event metrics panel will show you when an upload event fires and passes through to Azure Functions and Azure Batch
![Alt text](imgs/egs.png?raw=true "EventGrid Subscription Example")
You can further track detailed messages in the Azure Function logs as well as insights panel.

Upload a file into the input storage container and the cascade of events through the event grid and azure function should successfully submit a task in the job in the batch account.

You can use the [Azure Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/) and [Batch Explorer](https://azure.github.io/BatchExplorer/) to monitor job progress.