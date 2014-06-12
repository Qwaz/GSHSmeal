#encoding: utf-8

from functools import wraps

from django.shortcuts import redirect


def admin_login(func):
	@wraps(func)
	def wrapper(request, *args, **kwargs):
		if request.user.is_staff:
			return func(request, *args, **kwargs)
		else:
			return redirect('home')
	return wrapper
