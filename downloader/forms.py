# forms.py
from django import forms

class DownloadForm(forms.Form):
    video_url = forms.URLField(label='Enter the YouTube video URL', max_length=200,)
    quality_choices = [('highest', 'Highest'), ('lowest', 'Lowest')]
    quality = forms.ChoiceField(choices=quality_choices, initial='highest', widget=forms.RadioSelect)
