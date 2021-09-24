from rest_framework import authentication, exceptions, HTTP_HEADER_ENCODING
from django.contrib.auth import get_user_model
import firebase_admin
from firebase_admin import credentials, auth
import os
import json 
User = get_user_model()

saved_credential = os.getenv("FIREBASE_CRED")
cred = credentials.Certificate(json.loads(saved_credential))
firebase_admin.initialize_app(cred)
print('Firebase loaded')

def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.
    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth

class TokenAuthSupportQueryString(authentication.TokenAuthentication):
    """
    Extend the TokenAuthentication class to support querystring authentication
    in the form of "http://www.example.com/?access_token=<token_key>"
    """
    def authenticate(self, request):
        # Check if 'token_auth' is in the request query params.
        # Give precedence to 'Authorization' header.
        if 'access_token' in request.query_params and \
                        'HTTP_AUTHORIZATION' not in request.META:
            return self.authenticate_credentials(request.query_params.get('access_token'))
        else:
            return super(TokenAuthSupportQueryString, self).authenticate(request)

class FirebaseAuthentication(authentication.BaseAuthentication):
    """
    Authentication for firebase front-ends.
    Needs Authorization header in the form of "Firebase <token>" to work.
    """
    keyword = 'Firebase'

    def authenticate(self, request, **credentials):
        authheader = get_authorization_header(request)

        if not authheader:
            return None
        
        authheader = authheader.split()

        if not authheader or authheader[0].lower() != self.keyword.lower().encode():
            return None

        if len(authheader) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(authheader) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        token = authheader[1]
     
        try:
            decoded = auth.verify_id_token(token)
        except:
            raise exceptions.AuthenticationFailed('Token incorrect')
        
        try:
            user = User.objects.get(email=decoded["email"])
            if user.firebase_uid is None:
                user.firebase_uid = decoded["uid"]
                user.save()
        except User.DoesNotExist:
            try:
                user = User.objects.create_user(email=decoded["email"], firebase_uid=decoded["uid"])
            except:
                raise exceptions.AuthenticationFailed('User does not exist and cannot be created')

        return (user, decoded)