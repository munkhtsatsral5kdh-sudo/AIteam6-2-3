import gradio as gr
import google.generativeai as genai

# API тохиргоо - Таны ажиллаж байгаа түлхүүр
API_KEY = "AIzaSyCcybSAuvvOyXI_9T-63Bq0IQBPNhMJznM"
genai.configure(api_key=API_KEY)

def get_model():
    # 404 алдаанаас сэргийлж хамгийн тогтвортой загварыг сонгосон
    return genai.GenerativeModel('gemini-1.5-flash')

# ---- 1. Даалгавар үүсгэх функц ----
def generate_assignment(subject, topic, level):
    if not topic:
        return "Та хичээлийн сэдвээ бичнэ үү."
    
    prompt = f"""Чи бол {subject} хичээлийн мэргэжлийн багш. 
'{topic}' сэдвээр {level} түвшний 3 даалгавар бэлтгэ.
Сурагчдад ойлгомжтой Монгол хэлээр хариулж, хариуг нь тайлбартай оруулна уу.
Томьёог $...$ форматаар бичээрэй."""

    try:
        model = get_model()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Алдаа гарлаа: {str(e)}"

# ---- 2. Хариу шалгах функц ----
def check_answer(subject, topic, question, student_answer):
    if not question or not student_answer:
        return "Даалгавар болон сурагчийн хариуг хоёуланг нь бөглөнө үү."
    
    prompt = f"""Чи бол {subject} хичээлийн багш. Сурагчийн хариуг үнэл.
Сэдэв: {topic}
Даалгавар: {question}
Сурагчийн хариу: {student_answer}

Үнэлгээг дараах байдлаар гарга:
📊 Үнэлгээ: [Зөв/Буруу]
⭐ Оноо: [0-100]
💬 Тайлбар: [Яагаад ийм үнэлгээ өгсөн тухай]"""

    try:
        model = get_model()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Алдаа гарлаа: {str(e)}"

# ---- UI: Вэбсайтны бүтэц ----
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 Мөнхцацрал багшийн Ухаалаг Платформ")
    gr.Markdown("### 9 хичээлийн нэгдсэн туслах систем")

    subject_list = ["Монгол хэл", "Математик", "Физик", "Хими", "Биологи", "Газарзүй", "Нийгэм судлал", "Түүх", "Мэдээллийн технологи"]

    with gr.Tab("🚀 Даалгавар үүсгэх"):
        with gr.Row():
            with gr.Column():
                sub1 = gr.Dropdown(subject_list, label="📚 Хичээл сонгох", value="Монгол хэл")
                top1 = gr.Textbox(label="🔍 Сэдэв", placeholder="Жишээ нь: Жинхэнэ нэр")
                lev1 = gr.Radio(["⭐ Би чадна (Хялбар)", "⭐⭐ Би мэднэ (Дунд)", "⭐⭐⭐ Би мастер (Гүнзгий)"], label="Түвшин", value="⭐ Би чадна (Хялбар)")
                btn1 = gr.Button("🚀 Даалгавар үүсгэх", variant="primary")
            with gr.Column():
                out1 = gr.Markdown()
        btn1.click(fn=generate_assignment, inputs=[sub1, top1, lev1], outputs=out1)

    with gr.Tab("✅ Хариу шалгах"):
        with gr.Row():
            with gr.Column():
                sub2 = gr.Dropdown(subject_list, label="📚 Хичээл", value="Монгол хэл")
                top2 = gr.Textbox(label="🔍 Сэдэв", placeholder="Жишээ нь: Жинхэнэ нэр")
                q2 = gr.Textbox(label="❓ Даалгавар", placeholder="Даалгаврын текстийг энд тавь", lines=3)
                ans = gr.Textbox(label="✏️ Сурагчийн хариу", placeholder="Сурагч юу гэж хариулсныг энд тавь", lines=3)
                btn2 = gr.Button("✅ Шалгах", variant="primary")
            with gr.Column():
                out2 = gr.Markdown()
        btn2.click(fn=check_answer, inputs=[sub2, top2, q2, ans], outputs=out2)

if __name__ == "__main__":
    demo.launch()
