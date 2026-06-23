import json
from project.core.context_engineering import PromptTemplates
from project.core.observability import log_event
from project.memory.session_memory import SessionMemory
from project.tools.tools import web_search

class Worker:
    def __init__(self, memory: SessionMemory):
        self.memory = memory

    def generate_content(self, module: dict, trace_id: str) -> dict:
        log_event("Worker", "generate_content_start", trace_id, {"module_id": module.get("id")})
        
        title = module.get("title", "Topic")
        search_ctx = web_search(title)
        
        study_guide = f"""# {title}
        
## Core Explanation
This is a bite-sized guide covering {title}. 
It helps you understand the core mechanics and structure.
Here are some helpful details: {search_ctx}

## Active Practice Exercise
Write a small solution or explain how you would execute this concept in practice.
"""

        quiz = [
            {
                "question": f"What is the main objective of {title}?",
                "options": [
                    "To store variables",
                    "To structure learning workflow",
                    "To build operational models",
                    "All of the above"
                ],
                "correct_answer": "All of the above",
                "rubric": "Identify the multi-purpose utility of the concept."
            }
        ]
        
        response = {
            "study_guide": study_guide,
            "quiz": quiz
        }
        
        log_event("Worker", "generate_content_end", trace_id, {"module_id": module.get("id")})
        return response
