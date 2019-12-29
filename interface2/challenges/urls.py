from django.urls import path
from . import views

urlpatterns = [
    path('', views.challenges, name='challenges'),
    path('<int:challenge_id>/', views.challenge, name='challenge'),
]
