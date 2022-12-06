from django import forms
from django.contrib.auth import authenticate

class GenerateVoucherForm(forms.Form):

    voucher_key = forms.CharField(
        label="Voucher-Key-String", 
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your voucher key'})
        )

    voucher_count = forms.CharField(
        label="How many voucher?", 
        max_length=5,
        widget=forms.NumberInput(attrs={'class':'form-control','maxlength':'11','placeholder':'Number of voucher to be generated'})
        )
    

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'})
        )
    
    password = forms.CharField(
        label="Password",
        max_length=50,
        widget=forms.PasswordInput(attrs={'class':'form-control','style':'margin-top:8px','placeholder':'Password'})
        )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(student_id=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(student_id=username, password=password)
        return user   
    
    '''voucher_key = forms.CharField(
        label="Voucher-Key-String", 
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control'})
        )

    voucher_count = forms.CharField(
        label="How many voucher?", 
        max_length=5,
        widget=forms.NumberInput(attrs={'class':'form-control'})
        )'''