import gradio as gr
import google.generativeai as genai

# ТАНЫ ШИНЭ API ТҮЛХҮҮР
API_KEY = "AIzaSyDTDWwxVIK2NIE_6qTtRvHcnwpzIZo4shs"
genai.configure(api_key=API_KEY)

def generate_assignment(subject, topic, level):
    if not topic: return "Сэдвээ бичнэ үү."
    
    # 404 алдаанаас сэргийлж gemini-1.5-flash-latest ашиглалаа
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f"Чи бол {subject} хичээлийн багш. '{topic}' сэдвээр {level} түвшний 3 даалгавар бэлтгэж, хариуг нь тайлбарла. Монголоор хариул."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Алдаа: {str(e)}"

# Дизайн
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 Мөнхцацрал багшийн Ухаалаг Платформ")
    with gr.Row():
        with gr.Column():
            sub = gr.Dropdown(["Монгол хэл", "Математик", "Физик", "Хими", "Биологи", "Газарзүй", "Нийгэм судлал", "Түүх", "Мэдээллийн технологи"], label="📚 Хичээл", value="Монгол хэл")
            top = gr.Textbox(label="🔍 Сэдэв", placeholder="Жишээ нь: Жинхэнэ нэр")
            lev = gr.Radio(["⭐ Би чадна", "⭐⭐ Би мэднэ", "⭐⭐⭐ Би мастер"], label="Түвшин", value="⭐ Би чадна")
            btn = gr.Button("🚀 Даалгавар үүсгэх", variant="primary")
        out = gr.Markdown()
    btn.click(generate_assignment, [sub, top, lev], out)

demo.launch()
