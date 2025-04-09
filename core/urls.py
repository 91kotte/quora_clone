from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post-question/', views.post_question_view, name='post_question'),
    path('question/<int:pk>/', views.question_detail_view, name='question_detail'),
    path('like/<int:answer_id>/', views.like_answer_view, name='like_answer'),
    path('question/<int:pk>/answer/', views.post_answer_from_home_view, name='post_answer_from_home'),
    path('question/<int:pk>/edit/', views.edit_question, name='edit_question'),
    path('answer/<int:pk>/edit/', views.edit_answer, name='edit_answer'),
]
