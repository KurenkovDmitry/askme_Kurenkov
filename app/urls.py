from app import views
from django.urls import path


urlpatterns = [
    path('', views.index, name="index"),
    path('question/<int:give_question_id>/', views.question, name="question"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('edit/', views.settings, name="settings"),
    path('ask/', views.ask, name="ask"),
    path('hot/', views.hot, name="hot"),
    path('tag/<path:tag>', views.question_by_teg, name="question_by_teg"),
    path('like_dislike_question/', views.like_dislike_question, name='like_dislike_question'),
    path('like_dislike_answer/', views.like_dislike_answer, name='like_dislike_answer'),
    path('set-correct-answer/', views.set_correct_answer, name='set_correct_answer'),
    path('logout/', views.logout, name="logout")
]
