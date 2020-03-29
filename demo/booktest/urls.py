from django.conf.urls import url, include
# from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    # url(r'^booktest/$', views.IndexView.as_view()),
    # url(r'^book/$', views.BookView.as_view()),
    # restful 风格
    # url(r'^books/$', views.BooksAPIVIew.as_view()),
    # url(r'^books/(?P<pk>\d+)/$', views.BookAPIView.as_view())

    # DRF 的请求响应
    url(r'books/$', views.BookListAPIView.as_view()),
    # url(r'books/(?P<pk>\d+)/$', views.BookDetailAPIView.as_view()),



    # url(r'books/$', views.BookInfoViewSet.as_view({'get': 'list'})),  # book-list
    # url(r'books/(?P<pk>\d)/$', views.BookInfoViewSet.as_view({'get': 'retrieve'})),  # book-retrieve
    # url(r'books/latest/$', views.BookInfoViewSet.as_view({'get': 'latest'})),  # book-latest
    # url(r'books/(?P<pk>\d)/read/$', views.BookInfoViewSet.as_view({'put': 'read'})),  # book-read
    # url(r'', include(router.urls))
]
router = DefaultRouter()  # 可以处理视图的路由器
router.register(r'books', views.BookInfoViewSet)  # 向路由器中注册视图集

urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中

