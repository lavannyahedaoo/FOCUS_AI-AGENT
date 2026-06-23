import json
import os

class SessionMemory:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.profile_path = f"memory/profile_{user_id}.json"
        self.session_data = {
            "current_module_idx": 0,
            "session_transcript": [],
            "pending_quiz": None
        }
        self.load_profile()

    def load_profile(self):
        if os.path.exists(self.profile_path):
            try:
                with open(self.profile_path, "r") as f:
                    self.profile = json.load(f)
            except Exception:
                self.reset_profile()
        else:
            self.reset_profile()

    def reset_profile(self):
        self.profile = {
            "user_id": self.user_id,
            "learning_style": "default",
            "completed_modules": [],
            "active_module": None,
            "skill_mastery": {},
            "syllabus": None
        }
        self.save_profile()

    def save_profile(self):
        os.makedirs("memory", exist_ok=True)
        with open(self.profile_path, "w") as f:
            json.dump(self.profile, f, indent=2)

    def update_session(self, key, value):
        self.session_data[key] = value

    def get_session(self, key):
        return self.session_data.get(key)
