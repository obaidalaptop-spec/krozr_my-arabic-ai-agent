import streamlit as st
from groq import Groq

# --- الإعدادات ---
GROQ_API_KEY = "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"

# --- اطلب الاسم أول مرة ---
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if not st.session_state.user_name:
    st.title("بتحكي معي يقلبي ")
    name = st.text_input("شو اسم الحلو؟", placeholder="حط اسمك هون اغلبك...")
    if name:
        st.session_state.user_name = name
        st.rerun()  # يعيد تحميل الصفحة بعد ما يدخل الاسم
else:
    # --- إذا كان الاسم موجود، شغّل الشات ---
    st.title(f"خرافك معي يغالي {st.session_state.user_name}!")
    st.markdown("شوف انا بحاول افهمك بس تصعبهاش علي")

# --- استمرار المحادثة (مثل الكود السابق) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_ai_response(messages_list):
    client = Groq(api_key=GROQ_API_KEY)
    try:
        chat_completion = client.chat.completions.create(
            messages=messages_list,
            model="qwen/qwen3-32b",
            temperature=0.7,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

# --- عرض المحادثة ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- إدخال سؤال جديد ---
if st.session_state.user_name:  # بس يفتح الشات لو عنده اسم
    system_prompt = {
        "role": "system",
        "content": f"أنت تتحدث الآن مع {st.session_state.user_name}. خاطبه باسمه أحيانًا. أنت وكيل ذكاء اصطناعي عربي ودود. تحدث بالعربية فقط. افهم السياق الكامل للمحادثة. إذا قال '{st.session_state.user_name}' 'آه' أو 'أيوه'، فهم أن هذا رد على اقتراحك السابق."
    }

    if user_input := st.chat_input("اكتب رسالتك..."):
        # أضف رسالة المستخدم
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(f"**{st.session_state.user_name}:** {user_input}")

        # أضف رسالة النظام أول مرة
        if len(st.session_state.messages) == 1:
            full_messages = [system_prompt] + st.session_state.messages
        else:
            full_messages = st.session_state.messages

        # احصل على الرد
        with st.spinner("الوكيل يفكر..."):
            reply = get_ai_response(full_messages)

        # أضف الرد
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):

            st.markdown(reply)



