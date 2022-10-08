from django.shortcuts import render
# from django.http import HttpResponse


def index(request):
    return render(request, 'index.html', context={
        'hello': 'Приветствую тебя пользователь!',
    })
# def index(request):
#    return HttpResponse('Приветствую тебя пользователь!')
