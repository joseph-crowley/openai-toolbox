from django import forms

class InputForm(forms.Form):
    user_input = forms.CharField(label='Enter your message:', max_length=1024)

