import uuid
from decimal import Decimal

from django import forms


# Форма для обмена
class ExchangeForm(forms.Form):
    email = forms.EmailField(
        label='Email', 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'required': 'true'}))
    receiving_address = forms.CharField(
        label='Адрес или номер карты для получения',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'required': 'true',}))

    recipient_name = forms.CharField(
        label='Имя и фамилия получателя', 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'required': 'true'}))

    transaction_id = forms.CharField(widget=forms.HiddenInput(), initial=uuid.uuid4, required=False)
    selling_currency = forms.CharField(label='Что продаете', max_length=100, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    buying_currency = forms.CharField(label='Что покупаете', max_length=100, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    selling_amount = forms.CharField(label='Значение сколько продаете', max_length=20, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    buying_amount = forms.CharField(label='Значение сколько покупаете', max_length=20, widget=forms.TextInput(attrs={'readonly': 'readonly'}))


    def clean_selling_amount(self):
        data = self.cleaned_data['selling_amount']
        if isinstance(data, Decimal):
            return data
        try:
            return Decimal(str(data).replace(',', '.'))
        except ValueError:
            raise forms.ValidationError("Введите число.")

    def clean_buying_amount(self):
        data = self.cleaned_data['buying_amount']
        if isinstance(data, Decimal):
            return data
        try:
            return Decimal(str(data).replace(',', '.'))
        except ValueError:
            raise forms.ValidationError("Введите число.")

