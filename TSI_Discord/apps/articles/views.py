from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
import requests
from . import oauth_codes as oacode
from lib.processing.process_data import WebData
from lib.cogs.creatorOnly import creatorOnly
from lib.bot import bot


AUTH_URL = "https://discord.com/api/oauth2/authorize?client_id=783006663409139783&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Foauth2&response_type=code&scope=identify"
def index(request):
    return redirect(AUTH_URL)

def oauth2(request: HttpRequest) -> HttpResponse:
    global user_id
    code = request.GET.get('code')
    user = exchange_code(code)
    user_id = user['id']
    return render(request, 'articles/list.html')


def discord_login(request: HttpRequest):
    return redirect(AUTH_URL)


def exchange_code(code):
    data = {
        "client_id": oacode.CLIENT_ID,
        "client_secret": oacode.CLIENT_SECRET,
        "grant_type":"authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/oauth2",
        "scope": "identify"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    credentials = response.json()
    access_token = credentials['access_token']
    response = requests.get("https://discord.com/api/v6/users/@me", headers={
        'Authorization': 'Bearer %s' % access_token
    })
    user = response.json()
    return user

def studentInfo(request):
    st_name = request.POST.get('st_name', None)
    st_code = request.POST.get('code')
    # m = WebData(user_id, st_code, st_name)
    # m = creatorOnly(bot=bot, user_id=user_id, st_code=st_code, st_name=st_name)
    m = bot.get_cog("creatorOnly")
    access = m.process_data(user_id, st_code, st_name)
    # access = bot.process_data(user_id, st_code, st_name)

    if access:
        return HttpResponseRedirect( reverse('articles:access_granted'))
    else:
        return HttpResponseRedirect( reverse('articles:access_denied'))



def access_granted(request):
    return render(request, 'articles/access_grant.html')

def access_denied(request):
    return render(request, 'articles/access_deny.html')