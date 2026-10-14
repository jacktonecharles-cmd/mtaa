from django import forms

from .models import Business, Service, BusinessPhoto
from locations.models import Town, Area


class BusinessRegistrationForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = [
            "name", "category", "county", "town", "area",
            "description", "phone_number", "whatsapp_number", "email", "website",
            "address", "logo", "cover_image", "opening_hours",
            "facebook_url", "instagram_url", "tiktok_url", "twitter_url",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "opening_hours": forms.Textarea(
                attrs={"rows": 2, "placeholder": "Mon-Sat: 8:00 AM - 6:00 PM, Sun: Closed"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Town/Area options depend on County -- kept simple (all towns/areas
        # shown) for now; a JS-driven cascading filter can be added later.
        self.fields["town"].queryset = Town.objects.select_related("county")
        self.fields["area"].queryset = Area.objects.select_related("town")
        self.fields["area"].required = False

    def clean_logo(self):
        logo = self.cleaned_data.get("logo")
        if logo and logo.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Logo must be smaller than 5MB.")
        return logo

    def clean_cover_image(self):
        cover = self.cleaned_data.get("cover_image")
        if cover and cover.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Cover image must be smaller than 5MB.")
        return cover


class BusinessEditForm(BusinessRegistrationForm):
    """Same fields as registration; kept as a separate class so dashboard
    editing behaviour (e.g. re-triggering approval) can diverge later
    without touching the public registration form."""
    pass


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "description", "price", "image"]
        widgets = {"description": forms.Textarea(attrs={"rows": 2})}


class BusinessPhotoForm(forms.ModelForm):
    class Meta:
        model = BusinessPhoto
        fields = ["image", "caption"]
