from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder

project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint="https://meet-mbp1ks2o-eastus2.services.ai.azure.com/api/projects/meet-mbp1ks2o-eastus2_project")

agent = project.agents.get_agent("asst_c9qJN4SPfb0yBSmxFifTgSXe")

thread = project.agents.threads.get("thread_9cgyfQZLKF0qWZ0P4dJDA8v0")

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
