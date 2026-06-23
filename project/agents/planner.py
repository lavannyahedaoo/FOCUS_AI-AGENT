import json
import os
from project.core.context_engineering import PromptTemplates
from project.core.observability import log_event
from project.memory.session_memory import SessionMemory

class Planner:
    def __init__(self, memory: SessionMemory):
        self.memory = memory

    def generate_syllabus(self, goal: str, trace_id: str) -> dict:
        log_event("Planner", "generate_syllabus_start", trace_id, {"goal": goal})
        
        syllabus = {
            "syllabus": [
                {
                    "id": "mod_1",
                    "title": f"Introduction to {goal}",
                    "description": "Understand core concepts and set up your workspace.",
                    "duration": 15
                },
                {
                    "id": "mod_2",
                    "title": f"Variables and Data Types in {goal}",
                    "description": "Learn how values are stored, manipulated, and represented.",
                    "duration": 20
                },
                {
                    "id": "mod_3",
                    "title": f"Control Flow and Logical operations in {goal}",
                    "description": "Conditional statements, looping structures, and logic checks.",
                    "duration": 25
                }
            ]
        }
        
        log_event("Planner", "generate_syllabus_end", trace_id, {"modules_count": len(syllabus["syllabus"])})
        return syllabus
