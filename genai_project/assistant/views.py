import os
import fitz
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status

from backend.utils import get_text_from_file
from backend.summarizer import generate_summary
from backend.qa_engine import get_chunks, create_vector_store, get_qa_chain, answer_question
from backend.challenge import generate_logic_questions, generate_multiple_question_sets, evaluate_user_answer

# Global storage for uploaded document text
text_store = ""

# ------------------------ Upload Document ------------------------
class UploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        global text_store
        uploaded_file = request.data.get("file")

        if not uploaded_file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        os.makedirs("temp", exist_ok=True)
        file_path = os.path.join("temp", uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        text_store = get_text_from_file(file_path)

        return Response({"message": "File uploaded and text extracted successfully."})

# ------------------------ Generate Summary ------------------------
class SummaryView(APIView):
    def get(self, request):
        if not text_store:
            return Response({"error": "No document uploaded yet."}, status=400)
        summary = generate_summary(text_store)
        return Response({"summary": summary})

# ------------------------ Ask Anything ------------------------
class AskQuestionView(APIView):
    def post(self, request):
        question = request.data.get("question")
        if not question:
            return Response({"error": "No question provided."}, status=400)

        chunks = get_chunks(text_store)
        vectorstore = create_vector_store(chunks)
        qa_chain = get_qa_chain(vectorstore)
        answer = answer_question(question, qa_chain)

        return Response({"answer": answer})

# ------------------------ Challenge Me (3 Sets x 3 Questions) ------------------------
class ChallengeView(APIView):
    def get(self, request):
        global text_store

        if not text_store.strip():
            return Response({"error": "No document uploaded yet."}, status=400)

        try:
            print("[ChallengeView] Generating multiple question sets...")
            question_sets = generate_multiple_question_sets(text_store, num_sets=3, questions_per_set=3)
            print(f"[ChallengeView] Generated sets: {len(question_sets)}")
            return Response({"question_sets": question_sets})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)

# ------------------------ Evaluate User Answer ------------------------
class EvaluateAnswerView(APIView):
    def post(self, request):
        question = request.data.get("question")
        answer = request.data.get("answer")

        if not question or not answer:
            return Response({"error": "Both question and answer are required."}, status=400)

        feedback = evaluate_user_answer(question, answer, text_store)
        return Response({"feedback": feedback})
