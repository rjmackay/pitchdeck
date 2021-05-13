from django.urls import path

from .views import PitchUploadView

urlpatterns = [path("", PitchUploadView.as_view())]
