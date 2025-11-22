import streamlit as st
from groq import Groq

# --- الإعدادات ---
GROQ_API_KEY = "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"

# --- بدء سجل المحادثة لو ما موجودش ---
if "messages" not in st.session_state:
    st.session_state.messages = []

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
            model="llama-3.1-8b-instant",
            temperature=0.7,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

# --- واجهة الموقع ---
st.set_page_config(page_title="بوت كروزر", page_icon="🤖")
st.title("🤖 شو حكيت معي قبل")
st.markdown("كل سؤال وجواب يظهران في سجل دائم. المحادثة ما تتمسحش!")

# --- عرض الرسائل السابقة ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# --- في كماان اشي احكي تستحيش ---
if user_input := st.chat_input("احكيلي شو بدك بساعدك وانا معك..."):
    # أضف السؤال لسجل المحادثة
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    # حدد اللهجة
    dialect = detect_cultural_context(user_input)
    full_prompt = f"""
أنت وكيل ذكاء اصطناعي عربي. اللهجة: {dialect}.
السؤال: "{user_input}"
ارَد بالعربية فقط، بدون إنجليزي، وبشكل مباشر.
"""

    # احصل على الرد
    with st.spinner("الوكيل يفكر..."):
        reply = get_ai_response(full_prompt)

    # أضف الرد لسجل المحادثة
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)