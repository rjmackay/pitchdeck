from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from .forms import PitchUploadForm
from .models import PitchDeck


class PitchViewer(DetailView):
    def get_object(self, *args, **kwargs):
        try:
            return PitchDeck.objects.all().latest("created")
        except PitchDeck.DoesNotExist:
            return None

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect("upload")
        else:
            return super().get(*args, **kwargs)


class PitchUploadView(FormView):
    template_name = "core/pitchdeck_upload.html"
    form_class = PitchUploadForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.process_pitch()
        messages.success(self.request, "Pitch deck uploaded.")

        return super().form_valid(form)
