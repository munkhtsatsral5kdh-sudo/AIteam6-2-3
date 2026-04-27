import gradio as gr
import google.generativeai as genai

# API тохиргоо
genai.configure(api_key="AIzaSyCcybSAuvvOyXI_9T-63Bq0IQBPNhMJznM")

def generate_assignment(subject, topic, level):
    if not topic: return "Сэдвээ бичнэ үү."
    
    prompt = f"Чи бол {subject} хичээлийн багш. '{topic}' сэдвээр {level} түвшний 3 даалгавар бэлтгэж, хариуг нь оруулна уу."
    
    # Алдааг засах: Бүх боломжит загваруудыг шалгах жагсаалт
    test_models = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    for m_name in test_models:
        try:
            model = genai.GenerativeModel(m_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception:
            try:
                # Хэрэв дээрх болохгүй бол 'models/' гэж нэмж үзэх
                model = genai.GenerativeModel(f'models/{m_name}')
                response = model.generate_content(prompt)
                return response.text
            except Exception:
                continue # Дараагийн загвар руу шилжих
                
    return "AI загвар олдсонгүй. API түлхүүр тань идэвхгүй эсвэл бүс нутагт зөвшөөрөгдөөгүй байна."

# Вэбсайтны дизайн
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 Багшийн Ухаалаг Платформ")
    with gr.Row():
        with gr.Column():
            sub = gr.Dropdown(["Монгол хэл", "Математик", "Физик", "Хими", "Биологи", "Газарзүй", "Нийгэм судлал", "Түүх", "Мэдээллийн технологи"], label="📚 Хичээл", value="Монгол хэл")
            top = gr.Textbox(label="🔍 Сэдэв", placeholder="Жишээ нь: Жинхэнэ нэр")
            lev = gr.Radio(["⭐ Би чадна (Хялбар)", "⭐⭐ Би мэднэ (Дунд)", "⭐⭐⭐ Би мастер (Гүнзгий)"], label="Түвшин", value="⭐ Би чадна (Хялбар)")
            btn = gr.Button("🚀 Даалгавар үүсгэх", variant="primary")
        with gr.Column():
            out = gr.Markdown()
    btn.click(fn=generate_assignment, inputs=[sub, top, lev], outputs=out)

demo.launch()
