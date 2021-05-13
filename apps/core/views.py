from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from .forms import PitchUploadForm
from .models import PitchDeck


class PitchViewer(DetailView):
    def get_object(self, **kwargs):
        return PitchDeck.objects.all().latest("created")


class PitchUploadView(FormView):
    template_name = "core/pitchdeck_upload.html"
    form_class = PitchUploadForm
    success_url = "/"

    def form_valid(self, form):
        form.process_pitch()
        messages.success(self.request, "Pitch deck uploaded.")

        return super().form_valid(form)
