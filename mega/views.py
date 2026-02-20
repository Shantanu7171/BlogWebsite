from django.shortcuts import render

def h(request):
    return render(request,'websites/index.html')