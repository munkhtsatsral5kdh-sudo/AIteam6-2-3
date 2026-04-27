import gradio as gr
import google.generativeai as genai

# 1. API Түлхүүрээ энд солихоо мартав аа!
genai.configure(api_key="ТАНЫ_API_KEY_ЭНД")
model = genai.GenerativeModel('gemini-1.5-flash')

def universal_assignment_system(subject, topic, level):
    # AI-д өгөх заавар: Ямар ч хичээлд дасан зохицох чадвартай
    prompt = f"""
    Чи бол {subject} хичээлийн мэргэжлийн багш байна. 
    Сурагчдад зориулж "{topic}" сэдвээр {level} түвшний 3 даалгавар бэлтгэ.
    
    ШААРДЛАГА:
    1. Хичээлийн онцлогт тохирсон асуулт, дасгал байх.
    2. Хэрэв Математик бол томьёог $...$ форматаар бич.
    3. Хэрэв Гадаад хэл бол үгийн баялаг болон дүрмийн дасгал оруул.
    4. Хүүхдэд урам өгсөн Монгол хэлээр хариул.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Алдаа гарлаа: {str(e)}"

# Вэбсайтны дизайн
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 AI-д суурилсан Нэгдсэн Платформ")
    gr.Markdown("### 3-р хэсэг: Ухаалаг даалгаврын систем (Бүх хичээлээр)")
    
    with gr.Row():
        with gr.Column():
            # Хичээл сонгох хэсэг нэмэгдлээ
            subject_select = gr.Dropdown(
                ["Математик", "Монгол хэл", "Англи хэл", "Биологи", "Физик", "Түүх", "Газар зүй"], 
                label="📚 Хичээл сонгох", 
                value="Математик"
            )
            topic_input = gr.Textbox(label="🔍 Хичээлийн сэдэв", placeholder="Жишээ нь: Нарны систем, Эсийн бүтэц...")
            level_input = gr.Radio(
                ["⭐ Би чадна (Хялбар)", "⭐⭐ Би мэднэ (Дунд)", "⭐⭐⭐ Би мастер (Гүнзгий)"], 
                label="Түвшин сонгох", 
                value="⭐ Би чадна (Хялбар)"
            )
            submit_btn = gr.Button("✨ Даалгавар үүсгэх", variant="primary")
        
        with gr.Column():
            output_display = gr.Markdown(label="Үүссэн даалгавар")

    submit_btn.click(fn=universal_assignment_system, inputs=[subject_select, topic_input, level_input], outputs=output_display)

if __name__ == "__main__":
    demo.launch()
