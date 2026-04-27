import gradio as gr
import google.generativeai as genai

# Таны API түлхүүрийг энд шууд орууллаа
genai.configure(api_key="AIzaSyCcybSAuvvOyXI_9T-63Bq0IQBPNhMJznM")
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_assignment(subject, topic, level):
    if not topic:
        return "Та хичээлийн сэдвээ бичнэ үү."
    prompt = f"Чи бол {subject} хичээлийн багш. '{topic}' сэдвээр {level} түвшний 3 даалгавар бэлтгэ. Монголоор хариул."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Алдаа: {str(e)}"

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 Мөнхцацрал багшийн Ухаалаг Платформ")
    with gr.Row():
        with gr.Column():
            sub = gr.Dropdown(["Математик", "Монгол хэл", "Англи хэл", "Түүх", "Биологи", "Физик"], label="📚 Хичээл", value="Математик")
            top = gr.Textbox(label="🔍 Сэдэв", placeholder="Жишээ нь: Квадрат тэгшитгэл")
            lev = gr.Radio(["⭐ Би чадна", "⭐⭐ Би мэднэ", "⭐⭐⭐ Би мастер"], label="Түвшин", value="⭐ Би чадна")
            btn = gr.Button("🚀 Даалгавар үүсгэх", variant="primary")
        with gr.Column():
            out = gr.Markdown()
    btn.click(fn=generate_assignment, inputs=[sub, top, lev], outputs=out)

demo.launch()
