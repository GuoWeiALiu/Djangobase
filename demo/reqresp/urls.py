from django.conf.urls import url

from . import views

# urlpatterns是被django自动识别的路由列表变量
urlpatterns = [
    url(r'^weather/([a-z]+)/(\d{4})/$', views.weather),
    #url(r'^weather/(?P<city>[a-z]+)/(?P<year>\d{4})/$', views.weather),
    url(r'^response/$', views.demo_response)
]
