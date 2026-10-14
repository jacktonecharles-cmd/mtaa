from django import forms

from .models import Subscription


class SubscriptionRequestForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ["payment_reference"]
        widgets = {
            "payment_reference": forms.TextInput(
                attrs={"placeholder": "e.g. M-Pesa transaction code (optional for now)"}
            )
        }
