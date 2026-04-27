import gradio as gr
import google.generativeai as genai

# Таны шинэ API түлхүүр
API_KEY = "AIzaSyDTDWwxVIK2NIE_6qTtRvHcnwpzIZo4shs"
genai.configure(api_key=API_KEY)

def generate_assignment(subject, topic, level):
    if not topic: return "Сэдвээ бичнэ үү."
    
    # Алдаанаас бүрэн сэргийлэх: Боломжит бүх загварыг жагсааж шалгах
    available_models = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
    except:
        return "API түлхүүр буруу эсвэл идэвхгүй байна."

    if not available_models:
        return "Ашиглах боломжтой AI загвар олдсонгүй."

    # Хамгийн тохиромжтой загварыг сонгох (1.5-flash эсвэл pro)
    selected_model = available_models[0]
    for m in available_models:
        if 'gemini-1.5-flash' in m:
            selected_model = m
            break

    prompt = f"Чи бол {subject} хичээлийн багш. '{topic}' сэдвээр {level} түвшний 3 даалгавар бэлтгэж, хариуг нь тайлбарла. Монголоор хариул."
    
    try:
        model = genai.GenerativeModel(selected_model)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Алдаа гарлаа: {str(e)}"

# Дизайн
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 Мөнхцацрал багшийн Ухаалаг Платформ")
    with gr.Row():
        with gr.Column():
            sub = gr.Dropdown(["Монгол хэл", "Математик", "Физик", "Хими", "Биологи", "Газарзүй", "Нийгэм судлал", "Түүх", "Мэдээллийн технологи"], label="📚 Хичээл", value="Монгол хэл")
            top = gr.Textbox(label="🔍 Сэдэв")
            lev = gr.Radio(["⭐ Би чадна", "⭐⭐ Би мэднэ", "⭐⭐⭐ Би мастер"], label="Түвшин", value="⭐ Би чадна")
            btn = gr.Button("🚀 Даалгавар үүсгэх", variant="primary")
        out = gr.Markdown()
    btn.click(generate_assignment, [sub, top, lev], out)

demo.launch()
