import os
from dotenv import load_dotenv, find_dotenv
from openai import AzureOpenAI

load_dotenv(find_dotenv())

endpoint = os.environ["NEEL_AZURE_OPENAI_ENDPOINT"]
model_name = "gpt-4o-mini"
deployment = "gpt-4o-mini"

subscription_key = os.environ["NEEL_AZURE_OPENAI_API_KEY"]
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant. Use Bing Search where ever needed",
        },
        {
            "role": "user",
            "content": "Who won IPL 2025"
        }
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=deployment
)

print(response.choices[0].message.content)
