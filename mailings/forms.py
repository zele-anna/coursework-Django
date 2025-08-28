from django.forms import ModelForm
from django.forms.fields import BooleanField

from mailings.models import Mailing, Message, Recipient


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
        fields = ["message", 'recipient_list']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['recipient_list'].queryset = Recipient.objects.filter(owner=user)
            self.fields['message'].queryset = Message.objects.filter(owner=user)
