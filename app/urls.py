from app import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('question/<int:question_id>/', views.question, name="question"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('settings/', views.settings, name="settings"),
    path('ask/', views.ask, name="ask"),
    path('hot/', views.hot, name="hot"),
    path('tag/<path:tag>', views.question_by_teg, name="question_by_teg")
]