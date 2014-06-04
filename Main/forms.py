from django import forms


class BootstrapForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(BootstrapForm, self).__init__(*args, **kwargs)

		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control'})
			self.fields[field].widget.attrs.update({'id': field})


class LoginForm(BootstrapForm):
	id = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput, required=False)

	jsession_id = forms.CharField()
	m = forms.CharField(required=False)

	secure_id = forms.CharField(widget=forms.HiddenInput)
	secure_password = forms.CharField(widget=forms.HiddenInput)
