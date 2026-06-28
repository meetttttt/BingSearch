import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=os.environ["PROJECT_ENDPOINT"])

list_agents = project.agents.list_agents()

for index in list_agents:
    print(index)

