from django import forms


class PitchUploadForm(forms.Form):
    pitch_deck = forms.FileField(required=True)

    def process_pitch(self):
        # send email using the self.cleaned_data dictionary
        pass
