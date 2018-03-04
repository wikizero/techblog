"""techblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
import views
# import backend

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about', views.about_us),
    url(r'^full_page', views.full_page),
    url(r'^notes$', views.notes),
    url(r'^notes/login$', views.notes_login),
    url(r'^notes/logout$', views.notes_logout),
    url(r'^sign/in', views.sign_sys),
    url(r'^notes/share$', views.notes_share),
    url(r'^notes/details$', views.notes_details),

    url(r'^add/note', views.add_note),
    url(r'^get/note', views.get_note),
    url(r'^save/note', views.save_note),
    url(r'^del/note', views.del_note),

    url(r'^upload', views.upload),
    url(r'^download$', views.download),
    url(r'^remove', views.remove),

    url(r'^access/info', views.access_info),
    url(r'^message', views.message),

    # tools url
    url(r'^tool/pdf', views.tool_pdf),
    url(r'^download/music', views.download_music),
    url(r'^chat_room', views.chat_room),

]



