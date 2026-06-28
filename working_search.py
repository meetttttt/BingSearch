from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
from azure.ai.agents.models import MessageRole, BingGroundingTool
import time

import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=os.environ["PROJECT_ENDPOINT"])

agent = project.agents.get_agent(os.environ["AGENT_ID"])

# thread = project.agents.threads.get("thread_dEznu8qQ7taSNEA2uCWencZK")
thread = project.agents.threads.create()

while True:
    input_text = input("Enter your query: ")
    if input_text == 'q':
        break

    message = project.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"{input_text}",
        stream=True
    )
    start = time.time()
    run = project.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id)
    end = time.time()
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    else:
        # messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
        response_message = project.agents.messages.get_last_message_by_role(thread_id=thread.id, role=MessageRole.AGENT)

        if response_message:
            for text_message in response_message.text_messages:
                print(f"Agent response: {text_message.text.value}")

            for annotation in response_message.url_citation_annotations:
                print(f"URL Citation: [{annotation.url_citation.title}]({annotation.url_citation.url})")
        print(end-start)
