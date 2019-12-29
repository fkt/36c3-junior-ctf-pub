from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.http import JsonResponse

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Challenge
from .forms import FlagForm

@login_required(login_url='/accounts/login/')
@require_http_methods(['GET'])
def challenges(request):
    cur_user = User.objects.get(username=request.user)
    #challenges = Challenge.objects.filter(stage__lte=cur_user.stage)
    challenges = Challenge.objects.all()
    stage_challenges = {}
    for c in challenges:
        if not c.is_published:
            continue
        if stage_challenges.get(c.stage, None):
            stage_challenges[c.stage].append(c)
        else:
            stage_challenges[c.stage] = [c]
    solves = []
    for s in cur_user.solves.all():
        solves.append(s.id)

    return render(request, 'challenges/challenges.html', {'challenges': stage_challenges, 'solves': solves })


@login_required(login_url='/accounts/login/')
@require_http_methods(['POST', 'GET'])
def challenge(request, challenge_id):
    challenge = Challenge.objects.get(pk=challenge_id)
    if not challenge.is_published:
        return redirect('challenges')
    cur_user = User.objects.get(username=request.user)
    if cur_user.stage < challenge.stage:
        return redirect('challenges')
    if request.method == 'POST':
        form = FlagForm(request.POST)
        if form.is_valid():
            flag = form.cleaned_data['flag']
            if flag == challenge.flag:
                #cur_user.solves.add(challenge_id)
                #st = cur_user.stage
                #cur_user.stage = max(challenge.stage + 1, cur_user.stage)
                #if cur_user.stage > st:
                #    cur_user.stage_time = timezone.now()
                #cur_user.last_chal_time = timezone.now()
                #cur_user.save()

                return JsonResponse({'result': 'Correct :) but too late'})

        return redirect('challenge', challenge_id=challenge_id)
    else:
        form = FlagForm()
        solved = challenge in cur_user.solves.all()
        return render(request, 'challenges/challenge.html', {'form': form, 'challenge': challenge, 'solved': solved })

