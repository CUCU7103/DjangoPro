from django.shortcuts import render

# Create your views here.
def homeFunc(request):
    return render(request, "home.html")

#test 230610 jujuclubw