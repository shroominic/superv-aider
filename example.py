"""
This module implements a CrewAI-based software development workflow.

It sets up a hierarchical crew structure with a supervisor, manager, and developers
to generate, implement, and evaluate code tasks according to brand guidelines.
"""

from langchain_anthropic import ChatAnthropic
from src.config import GUIDELINES as guidelines
from crewai import Agent, Task, Crew, Process
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List
import os

def setup_environment():
    """Set up the environment by loading environment variables."""
    load_dotenv()

def create_model():
    """Create and return the ChatAnthropic model."""
    return ChatAnthropic(model='claude-3-5-sonnet-20240620')

class EvaluationResult(BaseModel):
    """Pydantic model for the output of the evaluation task."""
    task_description: str
    approved: bool
    reasoning: str
    generated_code: str

class SupervisorOutputModel(BaseModel):
    """Pydantic model for the output of the supervisor's evaluation."""
    result: List[EvaluationResult]

def create_agent(role: str, goal: str, backstory: str, model, allow_delegation: bool = True) -> Agent:
    """Create and return an agent with the given parameters."""
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        verbose=True,
        allow_delegation=allow_delegation,
        llm=model
    )

def create_task(description: str, expected_output: str, agent: Agent, output_json: BaseModel = None) -> Task:
    """Create and return a task with the given parameters."""
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        output_json=output_json
    )

def create_crew(agents: List[Agent], tasks: List[Task] = None, supervisor: Agent = None) -> Crew:
    """Create and return the crew with the given agents, tasks, and supervisor."""
    return Crew(
        agents=agents,
        tasks=tasks or [],
        process=Process.hierarchical,
        manager_llm=create_model(),  # Use the same model for the manager LLM
        verbose=2,
        manager=supervisor  # Set the supervisor as the manager agent (orchestrator)
    )
