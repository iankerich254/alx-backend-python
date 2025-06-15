from django.shortcuts import render, redirect

# Create your views here.
def delete_user(request):
    request.user.delete()
    return redirect('logout')
