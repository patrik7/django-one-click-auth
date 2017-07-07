import urllib

from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone

from one_click_auth.models import Token

from django.conf import settings


def auth(request, token, user_id, target_url):

	#make sure we have leading slash
	if len(target_url) == 0 or target_url[0] != '/':
		target_url = '/' + target_url


	#keep get params
	try:
		token = Token.objects.get(user_id=user_id, token=token, expires__gt=timezone.now())

		if request.user.is_authenticated:
			logout(request)

		if token.user.is_active:
			login(request, token.user)
		else:
			module_function = settings.ONE_CLICK_AUTH_SERIALIZE_USER.split('.')

			module = __import__('.'.join(module_function[:-1]), globals(), locals(), [module_function[-1]], -1)

			request.session['to_activate'] = getattr(module, module_function[-1])(token.user)

		if token.one_use:
			token.delete()

	except Token.DoesNotExist:
		pass

	if request.method == 'GET' and len(request.GET.keys()) > 0:
		params = urllib.urlencode(request.GET)

		return HttpResponseRedirect(target_url + "?%s" % params)
	else:
		return redirect(target_url)


def unsubscribe(request, token, user_id):
	#keep get params
	try:
		token = Token.objects.get(user_id=user_id, token=token, expires__gt=timezone.now())

		if request.user.is_authenticated:
			logout(request)

		module_function = settings.ONE_CLICK_AUTH_UNSUBSCRIBE.split('.')

		module = __import__('.'.join(module_function[:-1]), globals(), locals(), [module_function[-1]], -1)

		getattr(module, module_function[-1])(request, token.user)

		if token.one_use:
			token.delete()

	except Token.DoesNotExist:
		pass

	if request.method == 'GET' and len(request.GET.keys()) > 0:
		params = urllib.urlencode(request.GET)

		return HttpResponseRedirect('/' + "?%s" % params)
	else:
		return redirect('/')

