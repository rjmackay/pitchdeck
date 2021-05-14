from django.urls import path

from .views import PitchUploadView
from .views import PitchViewer

urlpatterns = [path("", PitchViewer.as_view(), name="home"), path("upload", PitchUploadView.as_view(), name="upload")]
