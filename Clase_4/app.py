import gradio as gr
 
def saludar(nombre):
    return f"Hola {nombre}"
 
demo = gr.Interface(fn=saludar, inputs="text", outputs="text")
demo.launch()
