from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Expense


class MultiFileInput(ClearableFileInput):
    allow_multiple_selected = True


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'city', 'province', 'amount']


class ReceiptUploadForm(forms.Form):
    images = forms.FileField(
        label="Scontrini (uno o più)",
        widget=MultiFileInput(attrs={'multiple': True}),
        required=False
    )
