# coding: utf-8
from django.shortcuts import render_to_response


def view(request):
    return render_to_response('index.html')