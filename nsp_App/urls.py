from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
                  path('', views.nseDataDownload.as_view(), name="nseDataDownload"),
                  path('symbolAPI', views.symbolDataAnalysis.as_view(), name="symbolData"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
