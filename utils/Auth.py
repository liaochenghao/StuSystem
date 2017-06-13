# coding:utf-8
from rest_framework import authentication


class SessionCsrfExemptAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return