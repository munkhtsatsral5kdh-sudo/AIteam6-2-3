import gradio as gr
import google.generativeai as genai

# 1. Өөрийн API түлхүүрийг доорх хашилтан дотор заавал хийгээрэй
genai.configure(api_key="ТАНЫ_API_KEY_ЭНД")
model = genai.GenerativeModel('gemini-1.5-flash')

# 3-р хэсэг: Даалгавар үүсгэх функц (Төлөвлөгөөний дагуу)
def create_math_task(topic, level):
    # Түвшний тайлбарыг AI-д өгөх зааварчилгаа
    level_desc = {
        "⭐ Би чадна (Хялбар)": "суурь ойлголтыг шалгасан 3 бодлого",
        "⭐⭐ Би мэднэ (Дунд)": "агуулгыг ашиглаж бодох 3 бодлого",
        "⭐⭐⭐ Би мастер (Гүнзгий)": "бүтээлч, логик сэтгэлгээ шаардсан 3 хүнд бодлого"
    }
    
    prompt = f"Чи бол Математикийн багшийн туслах байна. '{topic}' сэдвээр {level_desc[level]} бэлд. Томьёог заавал $...$ форматаар бичээрэй."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Алдаа гарлаа: {str(e)}"

# Вэбсайтны дизайн (Дизайн хэсэг)
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 AI-д суурилсан Ухаалаг даалгаврын систем")
    gr.Markdown("### Гүйцэтгэсэн: Э.Мөнхцацрал багш")
    
    with gr.Row():
        with gr.Column():
            topic_input = gr.Textbox(label="Хичээлийн сэдэв", placeholder="Жишээ нь: Квадрат тэгшитгэл")
            # Төлөвлөгөөнд тусгагдсан 3 түвшин
            level_input = gr.Radio(
                ["⭐ Би чадна (Хялбар)", "⭐⭐ Би мэднэ (Дунд)", "⭐⭐⭐ Би мастер (Гүнзгий)"], 
                label="Түвшин сонгох", 
                value="⭐ Би чадна (Хялбар)"
            )
            submit_btn = gr.Button("🚀 Даалгавар үүсгэх", variant="primary")
        
        with gr.Column():
            output_display = gr.Markdown(label="Үүссэн даалгавар")

    # Товчлуур дарах үед ажиллах холбоос
    submit_btn.click(fn=create_math_task, inputs=[topic_input, level_input], outputs=output_display)

if __name__ == "__main__":
    demo.launch()
