from django import forms
from .models import ContactMessage

from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["first_name", "last_name", "email", "subject", "message"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "id": "firstName",
                    "class": "form-input",
                    "placeholder": "محمد",
                    "required": True,
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "id": "lastName",
                    "class": "form-input",
                    "placeholder": "احمد",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "id": "email",
                    "class": "form-input",
                    "placeholder": "example@mail.com",
                    "required": True,
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "id": "subject",
                    "class": "form-input",
                    "placeholder": "كيف يمكننا مساعدتك؟",
                    "required": True,
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "id": "message",
                    "class": "form-textarea",
                    "placeholder": "اخبرنا المزيد عن استفسارك...",
                    "required": True,
                }
            ),
        }
