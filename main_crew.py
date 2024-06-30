from src.example import (
    setup_environment,
    create_model,
    create_agent,
    create_task,
    create_crew,
    SupervisorOutputModel,
    EvaluationResult
)

def main() -> SupervisorOutputModel:
    """
    Main function to run the CrewAI workflow.

    Returns:
        SupervisorOutputModel: The output model containing evaluation results.
    """
    setup_environment()
    model = create_model()
    
    from src.config import GUIDELINES

    from pydantic import BaseModel, Field, validator

    class TaskConfig(BaseModel):
        num_tasks: int = Field(..., ge=1, le=10)

        @validator('num_tasks')
        def validate_num_tasks(cls, v):
            if v < 1 or v > 10:
                raise ValueError('Number of tasks must be between 1 and 10')
            return v

    task_config = TaskConfig(num_tasks=1)  # You can change this number as needed

    # Feature Generation Crew
    feature_generator = create_agent(
        role='Feature Generator',
        goal=f'Generate {task_config.num_tasks} extremely simple and short code features (like a button or a banner). Just one-liners.',
        backstory=f"You are a manager responsible for creating the ticket for {task_config.num_tasks} very basic features that will be implemented.",
        model=model,
        allow_delegation=False
    )

    task_supervisor = create_agent(
        role='Task Supervisor',
        goal='Oversee the generation of tasks and ensure they are simple and appropriate.',
        backstory="You supervise the task generation process, ensuring tasks are suitable for implementation and evaluation.",
        model=model
    )

    generate_tasks = create_task(
        description=f"Generate {task_config.num_tasks} extremely simple and short code features for implementation.",
        expected_output=f"List of {task_config.num_tasks} simple tasks",
        agent=feature_generator
    )

    task_generation_crew = create_crew(
        agents=[feature_generator],
        tasks=[generate_tasks],
        supervisor=task_supervisor
    )

    # Main Crew
    supervisor = create_agent(
        role='Supervisor',
        goal='Oversee the evaluation of generated code and ensure it complies with the guidelines. DO NOT fix the code if it doesn\'t.',
        backstory="You are a high-level supervisor in the company. You oversee the evaluation process and ensure all generated code respects the company brand guidelines.",
        model=model
    )

    evaluator = create_agent(
        role='Code Evaluator',
        goal=f'Evaluate generated code for compliance with brand guidelines. Guidelines: {GUIDELINES}',
        backstory="You are a meticulous code evaluator responsible for ensuring all code adheres to company standards and maintains simplicity.",
        model=model,
        allow_delegation=False
    )

    manager = create_agent(
        role='Engineering Manager',
        goal='Specify the task for the developers. The tasks need to be as simple and small as possible. Once done, return the code - no need to verify anything.',
        backstory="You're an engineering manager responsible for getting the code for the assigned task. That's your only objective.",
        allow_delegation=True,
        model=model
    )
    
    backend_developer = create_agent(
        role='Backend Developer',
        goal='Generate code based on the manager\'s requirements. Keep it as simple as possible and make sure to JUST return code.',
        backstory="You're a backend developer. You generate very basic code based on the manager's specific requirements. You share the code that you generated when you're done.",
        model=model,
        allow_delegation=False
    )

    frontend_developer = create_agent(
        role='Frontend Developer',
        goal='Generate code based on the manager\'s requirements. Keep it as simple as possible and make sure to JUST return code.',
        backstory="You're a frontend developer. You generate very basic code based on the manager's specific requirements. You share the code that you generated when you're done.",
        model=model,
        allow_delegation=False
    )
    
    # Create main crew tasks
    implement_task = create_task(
        description="Implement a very simple feature for both backend and frontend. The feature should be as minimal as possible.",
        expected_output="Concatenated code implementing the feature for both backend and frontend",
        agent=manager
    )
    
    evaluate_task = create_task(
        description=f"Evaluate the generated code to see if it complies with the brand guidelines and meets the guidelines: {GUIDELINES}. Ensure the implementation is as simple as possible.",
        expected_output='{"task_description": "string", "approved": "bool", "reasoning": "string", "generated_code": "string"}',
        agent=evaluator,
        output_json=EvaluationResult
    )
    
    # Create main crew
    main_crew = create_crew(
        agents=[manager, evaluator, backend_developer, frontend_developer],
        tasks=[implement_task, evaluate_task],
        supervisor=supervisor
    )

    # Execute task generation
    tasks = task_generation_crew.kickoff()
    task = tasks

    # Execute main crew tasks for each generated task
    results = []
    # for task in tasks:
    implement_task.description = f"Implement this task: {task}"
    result = main_crew.kickoff()
    results.extend(result)

    supervisor_output = SupervisorOutputModel(result=results)

    # Save the supervisor's output to an external file
    import json
    with open('supervisor_output.json', 'w') as f:
        json.dump(supervisor_output.dict(), f, indent=2)

    return supervisor_output

if __name__ == "__main__":
    result = main()
    print("Supervisor output has been saved to 'supervisor_output.json'")
