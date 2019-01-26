from django.urls import path

from todolist import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('add/', views.AddTaskView.as_view(), name='add-task'),
    path('task/<slug:slug>', views.TaskDetailView.as_view(), name='task-detail'),
]
