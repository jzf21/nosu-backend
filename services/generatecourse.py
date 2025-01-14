import os
import json
from openai import OpenAI
from typing import List, Literal
from pydantic import BaseModel


# Define a schema for the Cybersecurity Syllabus
class Syllabus(BaseModel):
    module: str
    topics: List[str]
    difficulty: Literal["beginner", "intermediate", "advanced"]
    prerequisites: List[str]

class Content(BaseModel):
    topic: str
    content: str
    example: str
    difficulty: Literal["beginner", "intermediate", "advanced"]
    next_topic: List[str]
# Initialize OpenAI client
client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY"),
)

# Define messages for generating syllabus


def generate_syllabus():
    messages = [
        {
            "role": "system",
            "content": (
                "You are a teaching assistant specialized in designing cybersecurity courses. "
                "I will provide the learner's background, and you will generate a JSON syllabus "
                "with modules, topics, difficulty levels, and prerequisites for each module."
                """respond in this format {
    "module": "Introduction to Cybersecurity",
    "topics": [
        "Understanding Cybersecurity",
        "Cybersecurity Threat Landscape",
        "Cybersecurity Principles & Best Practices",
        "Whens & Whys of Cybersecurity"
    ],
    "difficulty": "beginner",
    "prerequisites": [
        "None"
    ]
}"""
            ),
        },
        {
            "role": "user",
            "content": (
                "The learner is a cybersecurity intermediate  topics like pentesting and wants advanced syllabus, "
                "JWT tokens, and cookies. Generate a syllabus for further learning."
            ),
        },
    ]

    # Generate syllabus with guided JSON
    completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-405B-Instruct",
        messages=messages,
        extra_body={"guided_json": Syllabus.model_json_schema()},
    )

    # Process output
    output = completion.choices[0].message
    if output.refusal:
        print(output.refusal)  # Handle refusal
    elif output.content:
        try:
            output_json = json.loads(output.content)
            print(json.dumps(output_json, indent=4))  # Pretty print JSON syllabus
        except Exception as e:
            print(f"Error parsing JSON: {e}")  # Handle JSON parsing errors


def generate_content(topic):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a teaching assistant specialized in explain cybersecurity topcis. "
                "given a topic you will provide a detailed explanation of the topic and real life examples of the topic."
                """respond in this format {
    "topic": "Introduction to Cybersecurity",
    "content":"this would contain detailed explanation of the topic"
    "example":"this would contain real life examples of the topic or practical examples"
    "difficulty": "beginner",
    "next_topic": [
        "SQL injection"
    ]
}"""
            ),
        },
        {
            "role": "user",
            "content": (
                "detailed info on" + topic
                
            ),
        },
    ]

    # Generate syllabus with guided JSON
    completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-405B-Instruct",
        messages=messages,
        extra_body={"guided_json": Content.model_json_schema()},
    )

    # Process output
    output = completion.choices[0].message
    if output.refusal:
        print(output.refusal)  # Handle refusal
    elif output.content:
        try:
            output_json = json.loads(output.content)
            print(json.dumps(output_json, indent=4))  # Pretty print JSON syllabus
        except Exception as e:
            print(f"Error parsing JSON: {e}")  # Handle JSON parsing errors
generate_content()
