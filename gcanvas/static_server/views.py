from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views.generic import View

class GCanvasView(View):
    def get(self, request, *args, **kwargs):
        if '/' == request.path or '/accounts/login/' == request.path:
            path = "/index.html"
        else:
            path = request.path.replace('accounts/login/', '')

        try:
            
            if path.endswith('png'):
                print(path)
                with open('build/web%s' % (path), 'rb') as p:
                    return HttpResponse(p.read(), mimetype="image/png")
            else:
                with open('build/web%s' % (path)) as p:
                    return HttpResponse(p.read())
        except IOError:
            raise Http404
        
        return HttpResponse("<h1>Page not fount</h1>")
        #render(
        #    request,
        #    'index.html',
        #    {}
        #)



