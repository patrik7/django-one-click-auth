=====
One Click Auth
=====

A simple app that allows easy generation of URLs that can be used to auth within django application. It uses the
standard django.contrib.auth to log users in.

It provides an easy wat to generate the links.

Furthemore, link usage can be limited to single use, or bounded by time. If links are invalid, you can still add user
information to the session and provide nice UX on the login form.

django.utils.crypto is used to generate links.

Quick start
-----------

1. Add "distance_matrix" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'one_click_auth',
    ]

2. Run `python manage.py migrate` to create the models.

3. Set up variables in settings.py::

    ONE_CLICK_AUTH_SERIALIZE_USER #OPTIONAL: function to call to serialize user to session
    ONE_CLICK_AUTH_UNSUBSCRIBE #OPTIONAL: function to call if users click on unsubscribe link

4. Route following URLs::

    url(r'^one-click-auth/(?P<token>[a-zA-Z0-9]+)/(?P<user_id>[0-9]+)/unsubscribe$', one_click_auth.views.unsubscribe, name='one_click_auth_unsubscribe'),
    url(r'^one-click-auth/(?P<token>[a-zA-Z0-9]+)/(?P<user_id>[0-9]+)/(?P<target_url>.*)', one_click_auth.views.auth, name='one_click_auth'),

Usage::

    token = Token(user=user)
    token.save()

    url_magic_link = token.auth_url(reverse('account') + '#change-password')
