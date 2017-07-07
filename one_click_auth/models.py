from __future__ import unicode_literals

from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from django.utils.crypto import get_random_string

DEFAULT_EXPIRE_DAYS=14


def default_token():
	return get_random_string(32)


def default_expires():
	return timezone.now() + timedelta(days=DEFAULT_EXPIRE_DAYS)


class Token(models.Model):
	token = models.CharField(max_length=32,null=False,default=default_token)
	user = models.ForeignKey(User)

	expires = models.DateTimeField(null=False,default=default_expires)

	one_use = models.BooleanField(null=False,default=False)

	def auth_url(self, url):
		#skip leading slash
		if len(url) > 0 and url[0] == '/':
			url = url[1:]

		return reverse('one_click_auth', kwargs={
			'token': self.token,
			'user_id': self.user.id,
			'target_url': url
		})

	def auth_unsubscribe(self):
		return reverse('one_click_auth_unsubscribe', kwargs={
			'token': self.token,
			'user_id': self.user.id,
		})