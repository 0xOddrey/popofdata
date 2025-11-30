from django.shortcuts import render


def home(request):
    return render(request, 'blog/index.html')


def qaiqai(request):
    return render(request, 'blog/qaiqai.html')


def beyonce(request):
    return render(request, 'blog/beyonce.html')


def launch(request):
    return render(request, 'blog/launch.html')
