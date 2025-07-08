import streamlit as st
import requests

# Page config
st.set_page_config(page_title="📄 GenAI Document Assistant", layout="wide")
st.title("📄 GenAI Document Assistant")

# Session setup
if "questions" not in st.session_state:
    st.session_state.questions = []
if "feedback" not in st.session_state:
    st.session_state.feedback = []
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ============================
# 🧰 Document Actions
# ============================
st.markdown("### 🧰 Document Actions")
col1, col2, col3 = st.columns(3)

# --------- Column 1: Upload ---------
with col1:
    st.subheader("📤 Upload")
    uploaded_file = st.file_uploader("Upload a .pdf or .txt", type=["pdf", "txt"])
    if uploaded_file:
        with st.spinner("Uploading and extracting text..."):
            res = requests.post("http://localhost:8000/api/upload/", files={"file": uploaded_file})
            if res.status_code == 200:
                st.success("✅ Uploaded!")
            else:
                st.error(f"❌ Upload failed: {res.json().get('error')}")

# --------- Column 2: Summary ---------
with col2:
    st.subheader("📝 Summary")
    if st.button("Get Summary"):
        res = requests.get("http://localhost:8000/api/summary/")
        if res.status_code == 200:
            st.markdown(f"**Summary:**\n\n{res.json()['summary']}")
        else:
            st.error("❌ Summary error: Please upload a document first.")

# --------- Column 3: Ask ---------
with col3:
    st.subheader("❓ Ask")
    question = st.text_input("Type your question...")
    if st.button("Get Answer"):
        res = requests.post("http://localhost:8000/api/ask/", json={"question": question})
        if res.status_code == 200:
            st.success(f"🧠 Answer: {res.json()['answer']}")
        else:
            st.error("❌ Unable to answer. Upload document first.")

# ============================
# 🚀 Challenge Mode
# ============================
st.markdown("---")
st.header("🚀 Challenge Mode")
num_q = st.slider("How many questions to attempt?", 1, 25, 10)

if st.button("Start Challenge"):
    res = requests.get("http://localhost:8000/api/challenge/")
    if res.status_code == 200:
        data = res.json()
        sets = data.get("question_sets", [])
        all_questions = []
        for qset in sets:
            all_questions.extend(qset.get("questions", []))

        st.session_state.questions = all_questions[:num_q]
        st.session_state.feedback = []
        st.session_state.submitted = False

        st.success(f"✅ Loaded {len(st.session_state.questions)} questions.")
    else:
        st.error("❌ Could not start challenge.")

# ============================
# 🧪 Display Questions
# ============================
if st.session_state.questions:
    st.markdown("### 🧪 Answer the questions below:")

    user_answers = []
    for i, q in enumerate(st.session_state.questions):
        st.markdown(f"#### Q{i+1}: {q['question']}")
        st.markdown(f"- **Type:** `{q.get('type', 'unknown')}`")
        st.markdown(f"- **Source:** _{q.get('justification', 'No justification provided')}_")
        user_input = st.text_input(f"Your Answer for Q{i+1}", key=f"user_answer_{i}")
        user_answers.append(user_input)

    if st.button("📬 Submit Answers"):
        all_feedback = []
        for i, ans in enumerate(user_answers):
            question_text = st.session_state.questions[i]["question"]
            res = requests.post("http://localhost:8000/api/evaluate/", json={
                "question": question_text,
                "answer": ans
            })
            if res.status_code == 200:
                feedback = res.json().get("feedback", "No feedback.")
            else:
                feedback = "Error evaluating answer."
            all_feedback.append(feedback)

        st.session_state.feedback = all_feedback
        st.session_state.submitted = True

# ============================
# 📊 Feedback Section
# ============================
if st.session_state.submitted:
    st.header("📊 Your Feedback")
    for i, fb in enumerate(st.session_state.feedback):
        correct = st.session_state.questions[i].get("answer", "")
        st.markdown(f"**Q{i+1}:** {fb}  \n✅ **Correct Answer:** `{correct}`")

# ============================
# 🔄 Reset
# ============================
if st.button("🔄 Reset Challenge"):
    st.session_state.questions = []
    st.session_state.feedback = []
    st.session_state.submitted = False
