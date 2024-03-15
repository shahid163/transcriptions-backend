from django.urls import path, re_path
from core import views

urlpatterns = [
    re_path(r'^upload/(?P<filename>[^/]+)$', views.FileUploadView.as_view(), name="upload"),
    re_path(r'^transcription/(?P<id>[^/]+)$', views.TranscriptionView.as_view(), name="transcription.get"),
]