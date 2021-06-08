from django.urls import path

from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('st', views.studentInfo, name = 'studentInfo'),
    path('oauth2', views.oauth2, name = "oauth2"),
    path('oauth2/login', views.discord_login, name="oauth_login"),
    path('access_granted', views.access_granted, name="access_granted"),
    path('access_denied', views.access_denied, name="access_denied")
]
