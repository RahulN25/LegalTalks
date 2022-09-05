from django.urls import path
from . import views as forum_views

app_name = 'forum'

urlpatterns = [
    path('', forum_views.search, name='search'),
    path('question/post/', forum_views.post_question, name='post-question'),
    path('question/<int:question_id>/', forum_views.question_detail, name='question-detail'),
    path('question/<int:question_id>/edit/', forum_views.edit_question, name='edit-question'),
    path('question/<int:question_id>/delete/', forum_views.question_delete, name='delete-question'),
    path('answer/edit/<int:answer_id>/', forum_views.edit_answer, name='edit-answer'),
    path('answer/delete/<int:answer_id>/', forum_views.delete_answer, name='delete-answer'),
    path('your-content/', forum_views.your_content, name='your-content'),
    path('anonymous/', forum_views.anonymous, name='anonymous'),
    path('vote/', forum_views.vote, name='vote'),
]