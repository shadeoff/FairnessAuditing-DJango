from django.urls import path

from . import views
from .views import Exp01View, Exp02View, Exp03View, Exp04View, Exp05View, Exp06View

urlpatterns = [
    path('index', views.index, name='index'),
    path("users/", views.create_user, name='users_create'),
    path("exp01/",Exp01View.as_view(), name='exp01'),
    path("exp02/",Exp02View.as_view(), name='exp02'),
    path("exp03/",Exp03View.as_view(), name='exp03'),
    path("exp04/",Exp04View.as_view(), name='exp04'),
    path("exp05/",Exp05View.as_view(), name='exp05'),
    path("exp06/",Exp06View.as_view(), name='exp06'),

]