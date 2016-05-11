from django import forms
from .models import Genre,Track

class FormForGenre(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ('Name',)

class TrackRequestForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ('Title','Stars','Genres',)
        widgets = {
        'Genres': forms.CheckboxSelectMultiple()
        }


