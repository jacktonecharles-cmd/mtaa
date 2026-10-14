from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(choices=[(i, f"{i} star{'s' if i != 1 else ''}") for i in range(5, 0, -1)]),
            "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "Share your experience..."}),
        }


class OwnerResponseForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["owner_response"]
        widgets = {"owner_response": forms.Textarea(attrs={"rows": 2})}
