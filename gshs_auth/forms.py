from django import forms

from utils.forms import BootstrapForm


class LoginForm(BootstrapForm):
	id = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput, required=False)

	jsession_id = forms.CharField(widget=forms.HiddenInput)
	m = forms.CharField(widget=forms.HiddenInput, required=False)

	secure_id = forms.CharField(widget=forms.HiddenInput)
	secure_password = forms.CharField(widget=forms.HiddenInput)
