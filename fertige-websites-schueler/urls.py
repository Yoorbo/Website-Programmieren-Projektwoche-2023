# -*- encoding: utf-8 -*-

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path

from .essentials import startup
from .views import *

urlpatterns = [
      path('websites/', programmierprojektmain, name='websites'),
      path('websites/<slug:slug>/', programmierprojektpages, name='websitesPage'),

      # Matches any html file
      re_path(r'^.*\.*', pages, name='pages')
  ] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
