# BingSearch

A collection of Python samples for working with **Azure AI Foundry Agents** and the
**Bing Grounding tool**. The scripts show how to create agents, ground their answers
in live Bing search results, hold multi-turn conversations, and expose an agent over a
small Flask HTTP API.

## Features

- Create an Azure AI agent wired up with the Bing Grounding tool (`git_ground_bing_agent.py`)
- Interactive chat loop against an existing agent with URL citations (`working_search.py`)
- Update an existing agent's instructions / temperature, then chat (`update_agents.py`)
- List all agents in a project (`list_all_agents.py`)
- Minimal one-shot query example (`main.py`)
- A Flask REST endpoint that proxies user queries to an agent (`api.py`)

## Requirements

- Python 3.9+
- An Azure AI Foundry project with a deployed model (e.g. `gpt-4o-mini`)
- A Bing Grounding connection configured on the project
- Azure credentials available to `DefaultAzureCredential` (e.g. via `az login`)

## Setup

```bash
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install azure-ai-projects azure-ai-agents azure-identity flask python-dotenv
```

### Configuration

Authentication uses `DefaultAzureCredential`, so sign in first:

```bash
az login
```

Create a `.env` file in the project root for any environment variables the scripts load
via `python-dotenv`:

```dotenv
PROJECT_ENDPOINT=https://<your-project>.services.ai.azure.com/api/projects/<your-project>
MODEL_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_BING_CONNECTION_ID=/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.MachineLearningServices/accounts/<account>/projects/<project>/connections/<connection-name>
```

> **Note:** Several scripts currently have the project endpoint, agent IDs, and Bing
> connection ID hardcoded. Replace those with your own values (or read them from `.env`)
> before running.

## Usage

Run any of the scripts directly:

```bash
# Create a Bing-grounded agent and run a sample query
python git_ground_bing_agent.py

# Interactive chat loop (type 'q' to quit)
python working_search.py

# Update an agent's instructions, then chat
python update_agents.py

# List all agents in the project
python list_all_agents.py

# Simple one-shot query
python main.py
```

### Flask API

Start the API server:

```bash
python api.py
```

Send a query:

```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Who won IPL 2025?"}'
```

Response:

```json
{
  "responses": [
    { "role": "user", "content": "Who won IPL 2025?" },
    { "role": "assistant", "content": "..." }
  ]
}
```

## Security

- Do **not** commit secrets. The `.env` file is excluded via `.gitignore`.
- Remove hardcoded credentials and resource IDs before sharing or deploying.
- The Flask app runs with `debug=True` for local development only — disable it in production.
