# assistant/models.py
from django.db import models

class UploadedDocument(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.file.name

class UserQuestion(models.Model):
    document = models.ForeignKey(UploadedDocument, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q: {self.question[:50]}..."

class ChallengeResponse(models.Model):
    document = models.ForeignKey(UploadedDocument, on_delete=models.CASCADE)
    question_text = models.TextField()
    user_answer = models.TextField()
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Challenge for: {self.document.file.name} ({self.created_at.date()})"
