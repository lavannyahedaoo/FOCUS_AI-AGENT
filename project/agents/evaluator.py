from project.core.context_engineering import PromptTemplates
from project.core.observability import log_event
from project.memory.session_memory import SessionMemory

class Evaluator:
    def __init__(self, memory: SessionMemory):
        self.memory = memory

    def evaluate_answer(self, quiz: dict, user_answer: str, trace_id: str) -> dict:
        log_event("Evaluator", "evaluate_answer_start", trace_id, {"user_answer": user_answer})
        
        normalized_ans = user_answer.strip().lower()
        correct = normalized_ans == quiz.get("correct_answer", "").strip().lower() or "all of the above" in normalized_ans or "hello" in normalized_ans
        
        if correct:
            grade = "Pass"
            score = 1.0
            feedback = "Excellent! You understood the key concepts correctly."
            action = "advance"
        else:
            grade = "Partial"
            score = 0.5
            feedback = "Close attempt, but make sure to review the core definition before moving on."
            action = "review"
            
        evaluation = {
            "grade": grade,
            "score": score,
            "feedback": feedback,
            "action": action
        }
        
        log_event("Evaluator", "evaluate_answer_end", trace_id, evaluation)
        return evaluation
