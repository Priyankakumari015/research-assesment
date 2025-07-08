from django.urls import path
from .views import UploadView, SummaryView, AskQuestionView, ChallengeView, EvaluateAnswerView

urlpatterns = [
    path('upload/', UploadView.as_view()),
    path('summary/', SummaryView.as_view()),
    path('ask/', AskQuestionView.as_view()),
    path("challenge/", ChallengeView.as_view(),name="challenge"),
    path('evaluate/', EvaluateAnswerView.as_view()),
]
