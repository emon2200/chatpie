from pathlib import Path
from django.views.static import serve
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static

from .import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api1/', include('api.urls')),
     path('api/', include('chatbot.urls')),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
