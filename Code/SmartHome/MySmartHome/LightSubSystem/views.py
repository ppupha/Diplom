from django.shortcuts import render
from django.views import View
from .models import TestLight

# Create your views here.
class IndexView(View):
    def get(self, request):
        lights = TestLight.objects.all()
        context = {'light': lights}
        print(lights)
        return render(request, 'index.html', context)
