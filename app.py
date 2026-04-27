import gradio as gr
import google.generativeai as genai
import os

# Таны шинэ API түлхүүр
API_KEY = "AIzaSyDTDWwxVIK2NIE_6qTtRvHcnwpzIZo4shs"
genai.configure(api_key=API_KEY)

def generate_assignment(subject, topic, level):
    if not topic: 
        return "⚠️ Сэдвээ бичнэ үү."
    
    # Хамгийн тогтвортой загварыг сонгох
    model_name = 'gemini-1.5-flash-latest'
    
    try:
        model = genai.GenerativeModel(model_name)
        prompt = f"Чи бол {subject} хичээлийн багш. '{topic}' сэдвээр {level} түвшний 3 даалгавар бэлтгэж, хариуг нь тайлбарла. Монголоор хариул."
        
        # Хариу ирэхийг хүлээж байгааг илтгэх
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text
        else:
            return "⚠️ AI хариу өгсөн боловч текст алга. Дахин оролдоно уу."
            
    except Exception as e:
        # Алдаа гарвал яг юу болсныг харуулна
        return f"❌ Алдаа гарлаа: {str(e)}\n\nЗөвлөмж: API түлхүүрээ зөв эсэхийг дахин шалгаарай."

# Вэб дизайн
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 Багшийн Ухаалаг Платформ")
    gr.Markdown("### 9 хичээлийн нэгдсэн туслах")
    
    with gr.Row():
        with gr.Column():
            sub = gr.Dropdown(["Монгол хэл", "Математик", "Физик", "Хими", "Биологи", "Газарзүй", "Нийгэм судлал", "Түүх", "Мэдээллийн технологи"], label="📚 Хичээл", value="Математик")
            top = gr.Textbox(label="🔍 Сэдэв", placeholder="Жишээ нь: Нэмэх үйлдэл")
            lev = gr.Radio(["⭐ Би чадна", "⭐⭐ Би мэднэ", "⭐⭐⭐ Би мастер"], label="Түвшин", value="⭐⭐⭐ Би мастер")
            btn = gr.Button("🚀 Даалгавар үүсгэх", variant="primary")
        
        # Хариу гарах хэсгийг тодорхой болгох
        with gr.Column():
            out = gr.Markdown(value="AI-ийн хариу энд гарна...")
            
    btn.click(fn=generate_assignment, inputs=[sub, top, lev], outputs=out)

demo.launch()
