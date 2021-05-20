from django.forms import ModelForm
from .models import *


class ConfirmOrderForm(ModelForm):

    class Meta:
        model = OrderModel
        fields = ['additional_note']
