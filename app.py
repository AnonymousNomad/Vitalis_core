import gradio as gr
def hello():
    return "Vitalis Core: Infrastructure Verified."
demo = gr.Interface(fn=hello, inputs=[], outputs="text")
demo.launch()
