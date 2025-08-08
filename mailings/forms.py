from django.forms import ModelForm
from django.forms.fields import BooleanField

from mailings.models import Recipient, Message, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class RecipientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Recipient
        exclude = ['owner']


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ['owner']


class MailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        exclude = ["sending_start", "sending_end", "status", 'owner']
