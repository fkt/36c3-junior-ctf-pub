from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.db.models import Count
from django.contrib.auth import get_user_model
User = get_user_model()

from .forms import RegisterForm

@require_http_methods(['POST', 'GET'])
def user_signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

@require_http_methods(['GET'])
def profile(request):
    return render(request, 'accounts/profile.html')

@require_http_methods(['GET'])
def scoreboard2(request):

    users = User.objects.all().filter(is_staff=False)
    try:
        cur_user = User.objects.get(username=request.user)
    except:
        cur_user = None
    users = users.annotate(count=Count('solves__id')).order_by('-count', 'last_chal_time')[:50]
    if cur_user in users:
        cur_user = None
    return render(request, 'accounts/scoreboard2.html',
            {'cur_user': cur_user, 'users': users})

@require_http_methods(['GET'])
def scoreboard_full2(request):

    users = User.objects.all().filter(is_staff=False)
    try:
        cur_user = User.objects.get(username=request.user)
    except:
        cur_user = None
    users = users.annotate(count=Count('solves__id')).order_by('-count', 'last_chal_time')
    if cur_user in users:
        cur_user = None
    return render(request, 'accounts/scoreboard2.html',
            {'cur_user': cur_user, 'users': users})

@require_http_methods(['GET'])
def scoreboard(request):

    users = User.objects.all().filter(is_staff=False)
    try:
        cur_user = User.objects.get(username=request.user)
    except:
        cur_user = None
    users = users.order_by('-stage', 'stage_time')[:20]
    if cur_user in users:
        cur_user = None
    return render(request, 'accounts/scoreboard.html',
            {'cur_user': cur_user, 'users': users})

@require_http_methods(['GET'])
def scoreboard_full(request):

    users = User.objects.all().filter(is_staff=False)
    try:
        cur_user = User.objects.get(username=request.user)
    except:
        cur_user = None
    users = users.order_by('-stage', 'stage_time')
    if cur_user in users:
        cur_user = None
    return render(request, 'accounts/scoreboard.html',
            {'cur_user': cur_user, 'users': users})

