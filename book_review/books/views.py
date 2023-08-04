from django.shortcuts import render


# Create your views here.
def main(request):
    return render(request, 'main.html')


def crud(request):
    return render(request, 'crud.html')
