import uuid
from project.agents.planner import Planner
from project.agents.worker import Worker
from project.agents.evaluator import Evaluator
from project.memory.session_memory import SessionMemory
from project.core.a2a_protocol import create_a2a_message, validate_a2a_message

class MainAgent:
    def __init__(self, user_id: str = "default_user"):
        self.memory = SessionMemory(user_id)
        self.planner = Planner(self.memory)
        self.worker = Worker(self.memory)
        self.evaluator = Evaluator(self.memory)

    def handle_message(self, user_input: str) -> dict:
        trace_id = f"trace_{uuid.uuid4().hex[:8]}"
        
        active_module_idx = self.memory.get_session("current_module_idx")
        pending_quiz = self.memory.get_session("pending_quiz")
        syllabus = self.memory.profile.get("syllabus")

        if not syllabus:
            syllabus_data = self.planner.generate_syllabus(user_input, trace_id)
            self.memory.profile["syllabus"] = syllabus_data["syllabus"]
            self.memory.save_profile()
            
            first_module = syllabus_data["syllabus"][0]
            content = self.worker.generate_content(first_module, trace_id)
            self.memory.update_session("pending_quiz", content["quiz"][0])
            
            response_text = (
                f"Welcome! I've created a study plan for you:\n"
                + "\n".join([f"- {m['title']}: {m['description']}" for m in syllabus_data["syllabus"]])
                + f"\n\n--- Active Lesson: {first_module['title']} ---\n"
                + content["study_guide"]
                + f"\n\nQuiz Time:\n{content['quiz'][0]['question']}\nOptions:\n"
                + "\n".join([f"  * {opt}" for opt in content['quiz'][0]['options']])
            )
            return {"response": response_text}

        if pending_quiz:
            evaluation = self.evaluator.evaluate_answer(pending_quiz, user_input, trace_id)
            self.memory.update_session("pending_quiz", None)
            
            if evaluation["action"] == "advance":
                next_idx = active_module_idx + 1
                self.memory.update_session("current_module_idx", next_idx)
                
                all_modules = self.memory.profile["syllabus"]
                if next_idx < len(all_modules):
                    next_mod = all_modules[next_idx]
                    content = self.worker.generate_content(next_mod, trace_id)
                    self.memory.update_session("pending_quiz", content["quiz"][0])
                    
                    response_text = (
                        f"Evaluation Feedback:\n{evaluation['feedback']}\n\n"
                        f"Moving on to next module: {next_mod['title']}\n"
                        f"{content['study_guide']}\n\n"
                        f"Quiz Time:\n{content['quiz'][0]['question']}\nOptions:\n"
                        + "\n".join([f"  * {opt}" for opt in content['quiz'][0]['options']])
                    )
                else:
                    response_text = f"Evaluation Feedback:\n{evaluation['feedback']}\n\nCongratulations! You have completed the entire course syllabus."
            else:
                curr_mod = self.memory.profile["syllabus"][active_module_idx]
                content = self.worker.generate_content(curr_mod, trace_id)
                self.memory.update_session("pending_quiz", content["quiz"][0])
                response_text = (
                    f"Evaluation Feedback:\n{evaluation['feedback']}\n\n"
                    f"Let's review this module once more:\n{content['study_guide']}\n\n"
                    f"Quiz:\n{content['quiz'][0]['question']}\nOptions:\n"
                    + "\n".join([f"  * {opt}" for opt in content['quiz'][0]['options']])
                )
            return {"response": response_text}

        return {"response": "You have completed your course! If you want to start a new subject, reset your memory."}

def run_agent(user_input: str):
    agent = MainAgent()
    result = agent.handle_message(user_input)
    return result["response"]
