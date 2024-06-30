"""FairnessAuditing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

urlpatterns = [
    path('api/csrf/', csrf_exempt(lambda request: JsonResponse({'csrfToken': get_token(request)})), name='csrf'),
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("api/", include('web.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    path('page01/',TemplateView.as_view(template_name='exp01.html'), name='exp01'),
    path('page02/',TemplateView.as_view(template_name='exp02.html'), name='exp02'),
    path('page03/',TemplateView.as_view(template_name='exp03.html'), name='exp03'),
    path('page04/',TemplateView.as_view(template_name='exp04.html'), name='exp04'),
    path('page05/',TemplateView.as_view(template_name='exp05.html'), name='exp05'),
    path('page06/',TemplateView.as_view(template_name='exp06.html'), name='exp06'),
]
