# Python
import oauth2 as oauth
import cgi

# Django
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from student.models import *

def buildDict(s):
	d = {}
	d['theStudent'] = s
	d['myClasses'] = s.classes.all()
	return d

# It's probably a good idea to put your consumer's OAuth token and
# OAuth secret into your project's settings.
consumer = oauth.Consumer(settings.GOOGLE_TOKEN, settings.GOOGLE_SECRET)
client = oauth.Client(consumer)

request_token_url = 'https://accounts.google.com/o/oauth2/auth'
access_token_url = 'https://accounts.google.com/o/oauth2/auth'

# This is the slightly different URL used to authenticate/authorize.
authenticate_url = 'https://accounts.google.com/o/oauth2/auth'

def google_login(request):
    # Step 1. Get a request token from Twitter.
    resp, content = client.request(request_token_url, "GET", "", {'response_type':"code",
															"scope":"email profile",
															"state":"email profile",
															"redirect_uri":"https://carat.bluemoonscience.com/login/authenticated/",
															"client_id":"767255874720-bo996qve1aicbhhvpkknmv588jed8b0e.apps.googleusercontent.com",
															"approval_prompt":"auto"})
    if resp['status'] != '200':
        raise Exception("Invalid response from Google.")

    # Step 2. Store the request token in a session for later use.
    request.session['request_token'] = dict(cgi.parse_qsl(content))

    # Step 3. Redirect the user to the authentication URL.
    url = "%s?oauth_token=%s" % (authenticate_url,
        request.session['request_token']['oauth_token'])

    return HttpResponseRedirect(url)


@login_required
def google_logout(request):
    # Log a user out using Django's logout function and redirect them
    # back to the homepage.
    logout(request)
    return HttpResponseRedirect('/')

def google_authenticated(request):
    # Step 1. Use the request token in the session to build a new client.
    token = oauth.Token(request.session['request_token']['oauth_token'],
        request.session['request_token']['oauth_token_secret'])
    client = oauth.Client(consumer, token)

    # Step 2. Request the authorized access token from Twitter.
    resp, content = client.request(access_token_url, "GET")
    if resp['status'] != '200':
        print content
        raise Exception("Invalid response from Google.")

    """
    This is what you'll get back from Twitter. Note that it includes the
    user's user_id and screen_name.
    {
        'oauth_token_secret': 'IcJXPiJh8be3BjDWW50uCY31chyhsMHEhqJVsphC3M',
        'user_id': '120889797', 
        'oauth_token': '120889797-H5zNnM3qE0iFoTTpNEHIz3noL9FKzXiOxwtnyVOD',
        'screen_name': 'heyismysiteup'
    }
    """
    access_token = dict(cgi.parse_qsl(content))

    # Step 3. Lookup the user or create them if they don't exist.
    try:
        user = User.objects.get(username = access_token['screen_name'])
    except User.DoesNotExist:
        # When creating the user I just use their screen_name@twitter.com
        # for their email and the oauth_token_secret for their password.
        # These two things will likely never be used. Alternatively, you
        # can prompt them for their email here. Either way, the password
        # should never be used.
        user = User.objects.create_user(access_token['screen_name'],
            '%s@twitter.com' % access_token['screen_name'],
            access_token['oauth_token_secret'])

        # Save our permanent token and secret for later.
        profile = Student()
        profile.user = user
        profile.oauth_token = access_token['oauth_token']
        profile.oauth_secret = access_token['oauth_token_secret']
        profile.save()

    # Authenticate the user and log them in using Django's pre-built
    # functions for these things.
    user = authenticate(username = access_token['screen_name'],
        password = access_token['oauth_token_secret'])
    login(request, user)

    return HttpResponseRedirect('/')
