from django.conf.urls import url, include

from . import views
from .views import DemoView

urlpatterns = [
    # 视图函数：注册
    # url(r'^register/$', views.register, name='register'),
    # 类视图：注册
    url(r'^register/$', views.DemoView.as_view(), name='register'),
    # url(路径, 视图),
    # url(r'^demoview1/$', views.DemoView.as_view()),
    #  在URL配置中装饰
    #url(r'^demoview2/$', views.my_decorator(DemoView.as_view())),
    url(r'^demoview/$', views.DemoView.as_view()),
]