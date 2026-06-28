from flask import Flask, request, jsonify
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
import os

# Flask app initialization
app = Flask(__name__)

# Hardcoded credentials (Not recommended for production)
TENANT_ID = "your-tenant-id"
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"

# Azure setup
credential = DefaultAzureCredential()

# Project and agent setup
endpoint = "https://meet-mbp1ks2o-eastus2.services.ai.azure.com/api/projects/meet-mbp1ks2o-eastus2_project"
project = AIProjectClient(credential=credential, endpoint=endpoint)
agent = project.agents.get_agent("asst_c9qJN4SPfb0yBSmxFifTgSXe")
thread = project.agents.threads.get("thread_dEznu8qQ7taSNEA2uCWencZK")


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
