from flask import Flask, request, jsonify
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Flask app initialization
app = Flask(__name__)

# Azure setup
credential = DefaultAzureCredential()

# Project and agent setup
endpoint = os.environ["PROJECT_ENDPOINT"]
project = AIProjectClient(credential=credential, endpoint=endpoint)
agent = project.agents.get_agent(os.environ["AGENT_ID"])
thread = project.agents.threads.get(os.environ["THREAD_ID"])


@app.route("/query", methods=["POST"])
def ask_agent():
    user_input = request.json.get("query")
    if not user_input:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    # Create a message
    message = project.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    # Run the agent
    run = project.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id
    )

    if run.status == "failed":
        return jsonify({"error": "Run failed", "details": run.last_error}), 500

    # Fetch messages
    messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    responses = [
        {"role": m.role, "content": m.text_messages[-1].text.value}
        for m in messages if m.text_messages
    ]

    return jsonify({"responses": responses})


if __name__ == "__main__":
    app.run(debug=True,
            host="0.0.0.0")
