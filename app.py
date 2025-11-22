import streamlit as st
from groq import Groq

# --- الإعدادات ---
GROQ_API_KEY = "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"

# --- بدء سجل المحادثة ---
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_ai_response(messages_list):
    client = Groq(api_key=GROQ_API_KEY)
    try:
        # نرسل كل المحادثة السابقة للنموذج — ده السر!
        chat_completion = client.chat.completions.create(
            messages=messages_list,
            model="moonshotai/kimi-k2-instruct-0905",
            temperature=0.7,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

# --- واجهة الموقع ---
st.set_page_config(page_title="krozr bot", page_icon="🤖")
st.title("🤖 وكيلك الذكي — محادثة ذكية")
st.markdown("الوكيل يفهم السياق! لما تقول 'آه'، يعرف إنك توافق على الاقتراح السابق.")

# --- عرض المحادثة ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- إدخال سؤال جديد ---
if user_input := st.chat_input("اكتب رسالتك..."):
    # أضف رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # أضف نظام تعليمات أول مرة
    if len(st.session_state.messages) == 1:
        system_msg = {
            "role": "system",
            "content": "أنت وكيل ذكاء اصطناعي عربي ودود. تحدث بالعربية فقط. افهم السياق الكامل للمحادثة. إذا قال المستخدم 'آه' أو 'أيوه'، فهم أن هذا رد على اقتراحك السابق. كن دافئًا ومبدعًا."
        }
        full_messages = [system_msg] + st.session_state.messages
    else:
        full_messages = st.session_state.messages

    # احصل على الرد
    with st.spinner("الوكيل يفكر..."):
        reply = get_ai_response(full_messages)

    # أضف الرد
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)