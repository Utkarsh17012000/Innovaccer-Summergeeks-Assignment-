from django import forms
from .models import Account,Meeting
from phonenumber_field.formfields import PhoneNumberField


class AccountForm(forms.ModelForm):
    name                =   forms.CharField(widget=forms.TextInput(attrs={'placeholder':'name'}))
    email               =   forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'email'}))
    password            =   forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    confirm_password    =   forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'confirm password'}))
    phone               =   PhoneNumberField(widget=forms.TextInput(attrs={'placeholder':'Phone'}))
    account_type        =   forms.CharField(widget=forms.TextInput(attrs={'placeholder':'visitor or host'}))

    class Meta:
        model=Account
        fields= "__all__"

class MeetingForm(forms.ModelForm):
    host_id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'hostid'}),label="hostid")
    check_in_time = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'placeholder':'HH:MM'},format=('%H:%M')))
    check_out_time = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'placeholder':'HH:MM'},format=('%H:%M')))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'address'}),label="address")

    class Meta:
        model = Meeting
        exclude = ['visitor_name','visitor_phone','timestamp']
        

        