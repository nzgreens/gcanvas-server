from django.shortcuts import render, redirect
from django.views.generic import View

class GCanvasView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'index.html',
            {}
        )



