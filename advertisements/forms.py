from django import forms

from .models import Advertisement


class AdvertisementRequestForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = [
            "title", "description", "image", "destination_url",
            "placement", "start_date", "end_date",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 2}),
        }

    def clean(self):
        cleaned = super().clean()
        start, end = cleaned.get("start_date"), cleaned.get("end_date")
        if start and end and end < start:
            raise forms.ValidationError("End date must be after the start date.")
        return cleaned
