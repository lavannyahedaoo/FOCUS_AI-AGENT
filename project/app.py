import gradio as gr
from project.main_agent import run_agent

def chat_interface(message, history):
    return run_agent(message)

demo = gr.ChatInterface(
    fn=chat_interface,
    title="FocusFlow AI",
    description="Your Multi-Agent Study Companion. Input your learning goal to get started!"
)

if __name__ == "__main__":
    demo.launch()
