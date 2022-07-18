
from django.shortcuts import render



def base_layout(request):
    return render(request, 'base_layout.html')