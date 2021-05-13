from django.views.generic.edit import FormView

from .forms import PitchUploadForm


class PitchUploadView(FormView):
    template_name = "pitch_upload.html"
    form_class = PitchUploadForm
    success_url = "/"

    def form_valid(self, form):
        form.process_pitch()
        return super().form_valid(form)
