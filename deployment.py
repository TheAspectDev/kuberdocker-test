import docker
from kubernetes import client, config
import os

BOT_TOKEN = os.getenv("BOT_TOKEN") 

client_docker = docker.from_env()
image, build_logs = client_docker.images.build(path="./bot", tag="bot-temp:latest", rm=True)

#kbconfig
config.load_kube_config()
v1 = client.CoreV1Api()


pod_manifest = client.V1Pod(
    metadata=client.V1ObjectMeta(name="bot-1"),
    spec=client.V1PodSpec(
        containers=[
            client.V1Container(
                name="bot-123",
                image="bot-temp:latest",
                env=[client.V1EnvVar(name="BOT_TOKEN", value=BOT_TOKEN)],
                resources=client.V1ResourceRequirements(
                    limits={"memory": "128Mi", "cpu": "100m"},
                    requests={"memory": "64Mi", "cpu": "50m"}
                )
            )
        ],
        restart_policy="Never" 
    )
)

v1.create_namespaced_pod(namespace="default", body=pod_manifest)
print('done')