import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=os.environ["PROJECT_ENDPOINT"])

agent = project.agents.get_agent(os.environ["AGENT_ID"])

thread = project.agents.threads.get(os.environ["THREAD_ID"])

message = project.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="Who won IPL 2025"
)

run = project.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id)

if run.status == "failed":
    print(f"Run failed: {run.last_error}")
else:
    messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)

    for message in messages:
        if message.text_messages:
            print(f"{message.role}: {message.text_messages[-1].text.value}")
