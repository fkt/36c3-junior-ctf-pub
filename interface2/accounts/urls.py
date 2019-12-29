from django.urls import path
from django.contrib.auth import views as admin_views
from . import views

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('scoreboard/', views.scoreboard, name='scoreboard'),
    path('scoreboard-c/', views.scoreboard2, name='scoreboard2'),
    path('scoreboard-full/', views.scoreboard_full, name='scoreboard_full'),
    path('scoreboard-full2/', views.scoreboard_full2, name='scoreboard_full2'),
    path('login/', admin_views.LoginView.as_view(), name='login'),
    path('logout/', admin_views.LogoutView.as_view(), name='logout'),
    path('password-change/',
        admin_views.PasswordChangeView.as_view(
            template_name='accounts/password_change_form.html'),
        name='password_change'),
    path('password-change/done/',
        admin_views.PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_done.html'),
        name='password_change_done'),
]
