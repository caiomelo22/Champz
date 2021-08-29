"""ChampzWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView

from WebApp import urls as WebAppUrls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(WebAppUrls)),
    path('webapp', TemplateView.as_view(template_name='teste.html')),
    path('webapp/matches', TemplateView.as_view(template_name='matches.html')),
]
