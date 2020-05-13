"""mateshelp_web URL Configuration

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
from django.conf.urls import url
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView


from rest_framework import routers
from locations import  views
from page_category import views as pageview

class IndexView(TemplateView):
    template_name = 'dist/index.html'

# register api endpoints
router = routers.DefaultRouter()
router.register(r'types', views.TypeViewSet)
router.register(r'locations', views.LocationViewSet)
router.register(r'pages', pageview.PageViewSet)

# register build as root, api & admin urls
urlpatterns = [
    path('',login_required(IndexView.as_view())),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    url(r'^accounts/login/$',LoginView.as_view(template_name='admin/login.html')),
    path('tinymce/', include('tinymce.urls')),
]
