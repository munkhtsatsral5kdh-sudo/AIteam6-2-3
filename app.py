import gradio as gr
from groq import Groq

import os
client = Groq(api_key=os.environ.get("API"))

def generate_assignment(subject, topic, level):
    if not topic:
        return "Сэдвээ бичнэ үү."
    
    level_map = {
        "⭐ Би чадна (Хялбар)": "хялбар",
        "⭐⭐ Би мэднэ (Дунд)": "дунд",
        "⭐⭐⭐ Би мастер (Гүнзгий)": "гүнзгий"
    }
    lv = level_map.get(level, "дунд")
    
    prompt = f"""Чи бол {subject} хичээлийн багш.
'{topic}' сэдвээр {lv} түвшний 3 даалгавар бэлтгэ.

Формат:
1️⃣ Даалгавар 1: [текст]
✅ Хариу 1: [хариу + тайлбар]

2️⃣ Даалгавар 2: [текст]
✅ Хариу 2: [хариу + тайлбар]

3️⃣ Даалгавар 3: [текст]
✅ Хариу 3: [хариу + тайлбар]"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message.content

def check_answer(subject, topic, question, student_answer):
    if not question or not student_answer:
        return "Даалгавар болон хариугаа бичнэ үү."
    
    prompt = f"""Чи бол {subject} хичээлийн багш. Сурагчийн хариуг үнэл.
Сэдэв: {topic}
Даалгавар: {question}
Сурагчийн хариу: {student_answer}

Формат:
📊 Үнэлгээ: [Зөв / Хэсэгчлэн зөв / Буруу]
⭐ Оноо: [0-100]
💬 Тайлбар: [юу зөв, юу буруу]
💡 Зөвлөмж: [хэрхэн сайжруулах]"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 Мөнхцацрал багшийн Ухаалаг Платформ")
    gr.Markdown("### Багшийн туслах: 9 хичээлийн нэгдсэн систем")

    subject_list = ["Монгол хэл", "Математик", "Физик", "Хими",
                    "Биологи", "Газарзүй", "Нийгэм судлал", "Түүх",
                    "Мэдээллийн технологи"]

    with gr.Tab("🚀 Даалгавар үүсгэх"):
        with gr.Row():
            with gr.Column():
                sub1 = gr.Dropdown(subject_list, label="📚 Хичээл", value="Монгол хэл")
                top1 = gr.Textbox(label="🔍 Сэдэв", placeholder="Жишээ нь: Язгуур")
                lev1 = gr.Radio(
                    ["⭐ Би чадна (Хялбар)", "⭐⭐ Би мэднэ (Дунд)", "⭐⭐⭐ Би мастер (Гүнзгий)"],
                    label="Түвшин", value="⭐ Би чадна (Хялбар)"
                )
                btn1 = gr.Button("🚀 Даалгавар үүсгэх", variant="primary")
            with gr.Column():
                out1 = gr.Markdown()
        btn1.click(fn=generate_assignment, inputs=[sub1, top1, lev1], outputs=out1)

    with gr.Tab("✅ Хариу шалгах"):
        with gr.Row():
            with gr.Column():
                sub2 = gr.Dropdown(subject_list, label="📚 Хичээл", value="Монгол хэл")
                top2 = gr.Textbox(label="🔍 Сэдэв", placeholder="Жишээ нь: Язгуур")
                q2   = gr.Textbox(label="❓ Даалгавар", lines=3)
                ans  = gr.Textbox(label="✏️ Сурагчийн хариу", lines=3)
                btn2 = gr.Button("✅ Шалгах", variant="primary")
            with gr.Column():
                out2 = gr.Markdown()
        btn2.click(fn=check_answer, inputs=[sub2, top2, q2, ans], outputs=out2)

demo.launch()
