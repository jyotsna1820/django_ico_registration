from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from captcha.fields import ReCaptchaField
from web3 import Web3

from .models import User, Subscription


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class UserAccountForm(forms.ModelForm):

    eth_address = forms.CharField(required=True, label='Contribution Address')
    eth_amount = forms.DecimalField(required=True, label='Contribution Amount')

    class Meta:
        model = User
        fields = ('eth_address', 'eth_amount', 'country')


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super(UserAccountForm, self).__init__(*args, **kwargs)

        self.fields['eth_address'].widget.attrs['placeholder'] = 'The ETH address you intend to contribute from'
        self.fields['eth_amount'].widget.attrs['placeholder'] = 'Amount of ETH you intend to contribute (0.1 ETH min)'

        self.fields['eth_address'].help_text = (
            '<div class="custom-help-block">eth address sample helptext</div>'
        )
        self.fields['eth_amount'].help_text = (
            '<div class="custom-help-block">eth amount example help text</div>'
        )

        if not self.user.editable:
            self.fields['eth_address'].widget.attrs['disabled'] = True
            self.fields['eth_amount'].widget.attrs['disabled'] = True
            self.fields['country'].widget.attrs['disabled'] = True

    def clean_eth_address(self):
        get_address = self.cleaned_data.get("eth_address")

        is_invalid = False
        try:
            eth_address = Web3.toChecksumAddress(get_address)
        except ValueError:
            is_invalid = True

        if is_invalid or not Web3.isAddress(eth_address):
            raise forms.ValidationError("Please enter a valid eth address")

        return eth_address

    def clean(self):
        cleaned_data = super().clean()

        if not all([
            self.data.get('check1') == 'on',
            self.data.get('check1') == 'on',
            self.data.get('check1') == 'on',
            self.data.get('check1') == 'on',
        ]):
            raise forms.ValidationError('Please check all the boxes above before continuing')

        return cleaned_data
