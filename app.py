import gradio as gr
import google.generativeai as genai

# Таны API түлхүүрийг энд тохирууллаа
genai.configure(api_key="AIzaSyCcybSAuvvOyXI_9T-63Bq0IQBPNhMJznM")
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_assignment(subject, topic, level):
    prompt = f"""
    Чи бол {subject} хичээлийн мэргэжлийн багш байна. 
    Сурагчдад зориулж "{topic}" сэдвээр {level} түвшний 3 даалгавар/бодлого бэлтгэ.
    Хүүхдэд урам өгсөн, маш ойлгомжтой Монгол хэлээр хариулж, бодолтыг нь оруулна уу.
    Хэрэв математик бол томьёог $...$ форматаар бичээрэй.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Алдаа гарлаа. Түлхүүр эсвэл холболтоо шалгана уу."

# Вэбсайтны дизайн - БҮХ ХИЧЭЭЛИЙГ СОНГОХ БОЛОМЖТОЙ
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 Мөнхцацрал багшийн Ухаалаг Платформ")
    gr.Markdown("### Багшийн туслах: Бүх хичээлээр даалгавар үүсгэх систем")
    
    with gr.Row():
        with gr.Column():
            # Багш ямар ч хичээл сонгох боломжтой хэсэг
            subject_select = gr.Dropdown(
                ["Математик", "Монгол хэл", "Англи хэл", "Биологи", "Физик", "Түүх", "Хими", "Газар зүй"], 
                label="📚 Хичээл сонгох", 
                value="Математик"
            )
            topic_input = gr.Textbox(label="🔍 Хичээлийн сэдэв", placeholder="Жишээ нь: Нарны систем, Тэгшитгэл...")
            level_input = gr.Radio(
                ["⭐ Би чадна (Хялбар)", "⭐⭐ Би мэднэ (Дунд)", "⭐⭐⭐ Би мастер (Гүнзгий)"], 
                label="Түвшин сонгох", 
                value="⭐ Би чадна (Хялбар)"
            )
            submit_btn = gr.Button("✨ Даалгавар үүсгэх", variant="primary")
        
        with gr.Column():
            output_display = gr.Markdown(label="Үүссэн даалгавар")

    submit_btn.click(fn=generate_assignment, inputs=[subject_select, topic_input, level_input], outputs=output_display)

if __name__ == "__main__":
    demo.launch()
