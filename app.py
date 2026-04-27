import gradio as gr
import google.generativeai as genai

# API тохиргоо
genai.configure(api_key="AIzaSyCcybSAuvvOyXI_9T-63Bq0IQBPNhMJznM")

def generate_assignment(subject, topic, level):
    if not topic: return "Сэдвээ бичнэ үү."
    
    prompt = f"Чи бол {subject} хичээлийн мэргэжлийн багш. '{topic}' сэдвээр {level} түвшний 3 даалгавар бэлтгэж, хариуг нь оруулна уу."
    
    # Алдаанаас сэргийлж 3 өөр нэрийг дарааллаар нь туршиж үзэх хэсэг
    model_names = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro']
    
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            response = model.generate_content(prompt)
            return response.text
        except Exception:
            continue # Хэрэв нэг нь болохгүй бол дараагийнхыг нь үзнэ
            
    return "Уучлаарай, AI загвартай холбогдож чадсангүй. Түлхүүр эсвэл бүс нутгийн хязгаарлалт байж магадгүй."

# Вэбсайтны дизайн
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 Мөнхцацрал багшийн Ухаалаг Платформ")
    gr.Markdown("### 9 хичээлийн нэгдсэн туслах")
    with gr.Row():
        with gr.Column():
            sub = gr.Dropdown(["Монгол хэл", "Математик", "Физик", "Хими", "Биологи", "Газарзүй", "Нийгэм судлал", "Түүх", "Мэдээллийн технологи"], label="📚 Хичээл", value="Математик")
            top = gr.Textbox(label="🔍 Сэдэв", placeholder="Жишээ нь: Зэрэг, Эсийн бүтэц")
            lev = gr.Radio(["⭐ Би чадна (Хялбар)", "⭐⭐ Би мэднэ (Дунд)", "⭐⭐⭐ Би мастер (Гүнзгий)"], label="Түвшин", value="⭐ Би чадна (Хялбар)")
            btn = gr.Button("🚀 Даалгавар үүсгэх", variant="primary")
        with gr.Column():
            out = gr.Markdown()
    btn.click(fn=generate_assignment, inputs=[sub, top, lev], outputs=out)

demo.launch()
