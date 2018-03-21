from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=256, widget=forms.PasswordInput())


class listingForm(forms.Form):
    item = forms.CharField(max_length=32)
    price = forms.CharField(max_length=32)
    user = forms.CharField(max_length=32)
    condition = forms.CharField(max_length=20)
    status = forms.CharField(max_length=20)



class SignUpForm(forms.Form):
    email = forms.EmailField(max_length=100)
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=256, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=256, widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

