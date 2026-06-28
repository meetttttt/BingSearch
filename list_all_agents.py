from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint="https://meet-mbp1ks2o-eastus2.services.ai.azure.com/api/projects/meet-mbp1ks2o-eastus2_project")

list_agents = project.agents.list_agents()

for index in list_agents:
    print(index)

