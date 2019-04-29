"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from app01 import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.testhandler.tcdm),
    url(r'^hadd/', views.testhandler.hadd),
    url(r'^gadd/', views.testhandler.gadd),
    url(r'^hdelete/(?P<id>\d+)', views.testhandler.hdelete),
    url(r'^gdelete/(?P<id>\d+)', views.testhandler.gdelete),
    url(r'^task/', views.testhandler.task),
    url(r'^check/', views.testhandler.check),
    url(r'^formatdata/', views.testhandler.formatdata),
    url(r'^envset.html$', views.testhandler.tenvset),
    url(r'^host.html$', views.testhandler.thost),
    url(r'^cmd.html$', views.testhandler.tcdm),
    url(r'^tsearch.html$', views.testhandler.tsearch),
    url(r'^help.html$', views.testhandler.help),
    url(r'^login/$', views.testhandler.login),
    url(r'^logout/$', views.testhandler.logout),
    url(r'^changpas/$', views.testhandler.changpas),
]
