"""apimockproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from apimock import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^mocked/$', views.mocked, name='mocked'),
    url(r'^mock/(?P<width>\d+)/$', views.mocked_param, name='mocked_param'),
    url(r'^mocked/', views.mocked_apis, name='mocked_apis'),
]
