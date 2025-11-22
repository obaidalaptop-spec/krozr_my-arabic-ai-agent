import streamlit as st
from groq import Groq

# --- إعدادات API ---
GROQ_API_KEY = "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"

def detect_cultural_context(text):
    text = text.lower()
    if any(word in text for word in ["ياخي", "والله", "شخبارك", "عيال"]):
        return "سعودي"
    elif any(word in text for word in ["يا عم", "إزيك", "بقى", "يا باشا"]):
        return "مصري"
    elif any(word in text for word in ["واخا", "بصح", "كاين", "راه"]):
        return "مغربي"
    else:
        return "عام"

def get_ai_response(prompt):
    client = Groq(api_key=GROQ_API_KEY)
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768",  #ا
            temperature=0.7,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ خطأ في الاتصال: {str(e)}"

# --- واجهة الموقع ---
st.set_page_config(page_title="وكيلك الذكي", page_icon="🤖", layout="centered")
st.title("🤖 عبيده بوت")
st.markdown("اعتبرني عبيده واحكي معي بحس فيك !")

user_msg = st.text_input("💬 انقلع اكتب شو بدك...", placeholder="مثال: انا بكره الحياه حس فيي...")

if user_msg:
    dialect = detect_cultural_context(user_msg)
    
    system_prompt = f"""
أنت وكيل ذكاء اصطناعي عربي. المستخدم يتحدث بلهجة {dialect}.
ارَد بالعربية فقط (فصحى أو دارجة طبيعية)، بدون أي كلمات إنجليزية.
كن دافئًا، متعاطفًا، واحترم الثقافة العربية.
السؤال: "{user_msg}"
الرد:
"""
    
    with st.spinner("الوكيل يفكّر... 🤔"):
        reply = get_ai_response(system_prompt)
    
    st.success("الوكيل:")
    st.markdown(f"> {reply}")

st.markdown("---")
st.caption("© 2025 | موقع ذكي بالعربي • مدعوم بـ Groq + Llama 3")