import gradio as gr
import google.generativeai as genai

# API түлхүүр тохиргоо
API_KEY = "AIzaSyCcybSAuvvOyXI_9T-63Bq0IQBPNhMJznM"
genai.configure(api_key=API_KEY)

def get_working_model():
    """Ажиллах боломжтой загварыг автоматаар хайж олох функц"""
    # Туршиж үзэх загваруудын нэрс
    models_to_test = [
        'gemini-1.5-flash', 
        'gemini-1.5-flash-latest', 
        'gemini-pro', 
        'models/gemini-1.5-flash',
        'models/gemini-pro'
    ]
    
    for m in models_to_test:
        try:
            model = genai.GenerativeModel(m)
            # Жижиг тест хийж үзэх
            model.generate_content("test", generation_config={"max_output_tokens": 1})
            return model
        except:
            continue
    return None

# ---- 1. Даалгавар үүсгэх ----
def generate_assignment(subject, topic, level):
    if not topic: return "Сэдвээ бичнэ үү."
    
    prompt = f"Чи бол {subject} хичээлийн багш. '{topic}' сэдвээр {level} түвшний 3 даалгавар бэлтгэж, хариуг тайлбартай бич. Монгол хэлээр хариул."
    
    try:
        model = get_working_model()
        if model is None:
            return "Алдаа: Таны API түлхүүр дээр ажиллах загвар олдсонгүй. AI Studio дээр түлхүүрээ шалгана уу."
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Системийн алдаа: {str(e)}"

# ---- 2. Хариу шалгах ----
def check_answer(subject, topic, question, student_answer):
    if not question or not student_answer: return "Мэдээллээ бүрэн оруулна уу."
    
    prompt = f"Багшийн хувиар сурагчийн хариултыг үнэлнэ үү.\nХичээл: {subject}\nСэдэв: {topic}\nАсуулт: {question}\nСурагчийн хариу: {student_answer}"
    
    try:
        model = get_working_model()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Алдаа: {str(e)}"

# ---- Гүйцэтгэх дизайн (UI) ----
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 Багшийн Ухаалаг Платформ")
    subjects = ["Монгол хэл", "Математик", "Физик", "Хими", "Биологи", "Газарзүй", "Нийгэм судлал", "Түүх", "Мэдээллийн технологи"]

    with gr.Tab("🚀 Даалгавар үүсгэх"):
        with gr.Row():
            with gr.Column():
                s1 = gr.Dropdown(subjects, label="Хичээл", value="Монгол хэл")
                t1 = gr.Textbox(label="Сэдэв")
                l1 = gr.Radio(["⭐ Хялбар", "⭐⭐ Дунд", "⭐⭐⭐ Гүнзгий"], label="Түвшин", value="⭐ Хялбар")
                btn1 = gr.Button("Үүсгэх", variant="primary")
            out1 = gr.Markdown()
        btn1.click(generate_assignment, [s1, t1, l1], out1)

    with gr.Tab("✅ Хариу шалгах"):
        with gr.Row():
            with gr.Column():
                s2 = gr.Dropdown(subjects, label="Хичээл")
                t2 = gr.Textbox(label="Сэдэв")
                q = gr.Textbox(label="Асуулт", lines=3)
                ans = gr.Textbox(label="Сурагчийн хариу", lines=3)
                btn2 = gr.Button("Шалгах")
            out2 = gr.Markdown()
        btn2.click(check_answer, [s2, t2, q, ans], out2)

demo.launch()
