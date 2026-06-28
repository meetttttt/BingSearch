import os
from openai import AzureOpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

endpoint = os.environ["MEET_AZURE_OPENAI_ENDPOINT"]
model_name = "gpt-4o-mini"
deployment = "gpt-4o-mini"

subscription_key = os.environ["MEET_AZURE_OPENAI_API_KEY"]
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
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "What is the stock price of Apple today"
        }
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=deployment
)

print(response.choices[0].message.content)
