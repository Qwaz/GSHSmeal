#encoding: utf-8
from django.shortcuts import render

from utils import update_today



# Create your views here.
def home(request):
	return render(request, 'home.html')


from django.http import HttpResponse


def test(request):
	update_today()
	return HttpResponse('updated')