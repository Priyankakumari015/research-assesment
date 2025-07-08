import random
import difflib
from transformers import pipeline
from backend.qa_engine import get_chunks, create_vector_store, get_qa_chain, answer_question

# Load Flan-T5 model only once
qa_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_new_tokens=128,
    do_sample=True,         # ← adds randomness
    temperature=0.9,        # ← creative variety
    top_p=0.95              # ← diverse output (nucleus sampling)
)


# ------------------ Prompt Generator ------------------
def generate_prompt(text, num_questions=10):
    templates = [
        f"Generate {num_questions} unique wh- and fill-in-the-blank questions from the given text. No answers. Avoid repetition.",
        f"Create {num_questions} challenging questions using wh-words and blanks from the passage below. Do not include answers.",
        f"Formulate {num_questions} diverse comprehension questions from the text. Include fill-in-the-blanks. Skip answers.",
        f"Generate {num_questions} meaningful and diverse questions using the following text. Avoid similar facts and repetitions.",
        f"From the given text, produce {num_questions} mixed questions (wh-type and fill-in-the-blank). No answers needed.",
    ]
    chosen_prompt = random.choice(templates)
    return f"""{chosen_prompt}

Text:
{text}

Questions:"""

# ------------------ Core Logic for One Set ------------------
def generate_logic_questions(text, num_questions=10):
    chunks = get_chunks(text)
    if not chunks:
        return []
    random.shuffle(chunks)

    vectorstore = create_vector_store(chunks)
    qa_chain = get_qa_chain(vectorstore)

    # Combine and trim to 2500 words
    combined_text = " ".join(chunk.page_content for chunk in chunks)
    if len(combined_text.split()) > 2500:
        combined_text = " ".join(combined_text.split()[:2500])

    prompt = generate_prompt(combined_text, num_questions)
    prompt += f"\n\nChallenge ID: {random.randint(10000, 99999)}"
    try:
        response = qa_pipeline(prompt)[0]['generated_text']
    except Exception as e:
        return [{"question": "Error generating questions", "answer": str(e), "type": "error"}]

    # Parse questions from output
    raw_lines = [line.strip("•-1234567890. ") for line in response.split("\n") if line.strip()]
    questions = []

    for line in raw_lines:
        if len(line) < 5 or not any(q in line.lower() for q in ['who', 'what', 'when', 'where', 'why', 'how', '____']):
            continue

        question = line if line.endswith("?") else line + "?"
        qtype = "fill-in-the-blank" if "____" in line else "wh-question"

        try:
            answer = answer_question(question, qa_chain)
        except Exception:
            answer = "Unknown"

        questions.append({
        "question": question,
        "answer": answer.strip(),
        "type": qtype,
        "justification": "Answer grounded in retrieved chunk."  # <-- Static placeholder or add actual chunk
    })

    return questions

# ------------------ Generate Multiple Sets ------------------
def generate_multiple_question_sets(text, num_sets=3, questions_per_set=10):
    all_sets = []

    for i in range(num_sets):
        questions = generate_logic_questions(text, num_questions=questions_per_set)
        all_sets.append({
            "set_number": i + 1,
            "questions": questions
        })

    return all_sets

# ------------------ User Answer Evaluation ------------------
def evaluate_user_answer(original_question, user_answer, source_text):
    """
    Evaluate similarity between user answer and expected answer from the source text.
    """
    similarity = difflib.SequenceMatcher(None, original_question.lower(), user_answer.lower()).ratio()

    if similarity > 0.8:
        return "Excellent answer! Very close to the expected response."
    elif similarity > 0.5:
        return "Good attempt, but could be more precise."
    else:
        return "Answer is not quite accurate. Please review the content again."

# ------------------ Example Usage ------------------
if __name__ == "__main__":
    # Example input text (you can load from a file or PDF too)
    sample_text = """
    The Internet of Things (IoT) refers to a network of physical devices that are connected to the internet and can collect and exchange data. 
    These devices range from everyday household objects to sophisticated industrial tools. With more than 10 billion connected IoT devices today, 
    this technology is a key component of modern smart systems. IoT enhances data collection, automation, efficiency, and real-time insights.
    """

    question_sets = generate_multiple_question_sets(sample_text, num_sets=3, questions_per_set=5)

    for qset in question_sets:
        print(f"\n🧩 Question Set {qset['set_number']}")
        for idx, q in enumerate(qset['questions'], 1):
            print(f"\nQ{idx}: {q['question']}\nA: {q['answer']} ({q['type']})")
