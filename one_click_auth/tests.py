from django.contrib.auth.models import User
from django.test import TestCase

from one_click_auth.models import Token


class AuthUsingLink(TestCase):


	def setUp(self):
		super(AuthUsingLink, self).setUp()

		self.user = User.objects.create_user('__test__auth__', password='password', email='auth@auth.com')
		self.user.save()

		self.token = Token(user=self.user)
		self.token.save()


	def tearDown(self):
		self.token.delete()
		self.user.delete()

		super(AuthUsingLink, self).tearDown()


	def test_one_click_auth(self):
		url = self.token.auth_url(url='/') #assumes webapp has a homepage

		result = self.client.get(url, follow=True)
		self.assertEqual(result.status_code, 200)
