import gradio as gr
import google.generativeai as genai

# API тохиргоо
genai.configure(api_key="AIzaSyCcybSAuvvOyXI_9T-63Bq0IQBPNhMJznM")
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_assignment(subject, topic, level):
    if not topic:
        return "Та хичээлийн сэдвээ бичнэ үү."
        
    prompt = f"""
    Чи бол {subject} хичээлийн мэргэжлийн багш байна. 
    Сурагчдад зориулж "{topic}" сэдвээр {level} түвшний 3 даалгавар бэлтгэ.
    Монгол хэлээр хариулж, бодолт эсвэл хариуг нь оруулна уу.
    Математик, Физик, Химийн томьёог $...$ форматаар бичээрэй.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Алдаа: {str(e)}"

# Вэбсайтны дизайн
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 Мөнхцацрал багшийн Ухаалаг Платформ")
    gr.Markdown("### Багшийн туслах: 9 хичээлийн нэгдсэн систем")
    
    with gr.Row():
        with gr.Column():
            subject_select = gr.Dropdown(
                ["Монгол хэл", "Математик", "Физик", "Хими", "Биологи", "Газарзүй", "Нийгэм судлал", "Түүх", "Мэдээллийн технологи"], 
                label="📚 Хичээл сонгох", 
                value="Монгол хэл"
            )
            topic_input = gr.Textbox(label="🔍 Сэдэв", placeholder="Жишээ нь: Жинхэнэ нэр")
            level_input = gr.Radio(
                ["⭐ Би чадна (Хялбар)", "⭐⭐ Би мэднэ (Дунд)", "⭐⭐⭐ Би мастер (Гүнзгий)"], 
                label="Түвшин", 
                value="⭐ Би чадна (Хялбар)"
            )
            submit_btn = gr.Button("🚀 Даалгавар үүсгэх", variant="primary")
        
        with gr.Column():
            output_display = gr.Markdown()

    submit_btn.click(fn=generate_assignment, inputs=[subject_select, topic_input, level_input], outputs=output_display)

demo.launch()
