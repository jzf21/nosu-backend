from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel, Field
from typing import List, Literal
from openai import OpenAI
import os
import json
router = APIRouter()


class CourseRequest(BaseModel):
    topic: str


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

class Quiz(BaseModel):
    question: str
    options: List[str]
    answer: str
# Initialize OpenAI client
client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY"),
)

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
            return output_json
            print(json.dumps(output_json, indent=4))  # Pretty print JSON syllabus
        except Exception as e:
            print(f"Error parsing JSON: {e}")  # Handle JSON parsing errors


def generate_quiz(topic):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a teaching assistant specialized in creating quizzes for cybersecurity courses. "
                "Given a topic, generate 5 quiz questions with multiple choice options and correct answers. "
                """respond in this format {
    "questions": [
        {
            "question": "What is the purpose of a firewall?",
            "options": [
                "To protect against malware",
                "To monitor network traffic",
                "To filter incoming and outgoing traffic",
                "To secure user data"
            ],
            "answer": "To filter incoming and outgoing traffic"
        }
    ]
}
Please generate exactly 5 questions."""
            ),
        },
        {"role": "user", "content": f"Generate 5 quiz questions on {topic}"},
    ]

    completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-405B-Instruct",
        messages=messages,
        max_tokens=1000,  # Increase token limit for multiple questions
        temperature=0.7,
        extra_body={
            "guided_json": {
                "type": "object",
                "properties": {
                    "questions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "question": {"type": "string"},
                                "options": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "minItems": 4,
                                    "maxItems": 4,
                                },
                                "answer": {"type": "string"},
                            },
                            "required": ["question", "options", "answer"],
                        },
                        "minItems": 5,
                        "maxItems": 5,
                    }
                },
            }
        },
    )

    output = completion.choices[0].message
    if output.refusal:
        raise ValueError(output.refusal)
    elif output.content:
        try:
            output_json = json.loads(output.content)
            if len(output_json.get("questions", [])) != 5:
                raise ValueError("Invalid number of questions generated")
            return output_json
        except Exception as e:
            raise ValueError(f"Error parsing quiz JSON: {e}")
    return None


@router.post("/course", response_model=None)
def generate_course(request: CourseRequest):
    content = generate_content(request.topic)
    return content


@router.post("/quiz", response_model=None)
def generate_questions(
    response: Response,
    topic: str,
):
    quiz = generate_quiz(topic)
    return quiz
