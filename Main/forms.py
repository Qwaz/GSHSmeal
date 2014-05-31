from django import forms


class BootstrapForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(BootstrapForm, self).__init__(*args, **kwargs)

		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control'})


class LoginForm(BootstrapForm):
	id = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	identifier = forms.CharField(widget=forms.HiddenInput)