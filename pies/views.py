from django.shortcuts import render,redirect, HttpResponse
from django.contrib import messages
from . import models


def pies(request):
    if request.session['is_logged_in'] is True:
        logged_user = models.get_user_by_email(request.session['user_email'])
        context = {
            'user' : logged_user[0],
            'pies' : models.get_all_pies()
        }
        return render(request, "pies.html", context)
    else:
        return HttpResponse("Who are you ?!!")
    
def create_pie(request):
    if request.method == "POST":
        errors = models.Pie.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/dashboard')
        else:
            logged_user = models.get_user_by_email(request.session['user_email'])
            models.create_pie(request.POST, logged_user[0])
            return redirect('/dashboard')

    else:
        return HttpResponse("Something went wrong!")

def delete_pie(request):
    if request.method == "POST":
        logged_user = models.get_user_by_email(request.session['user_email'])
        models.delete_pie(request.POST, logged_user[0])
        return redirect('/dashboard')

    else:
        return HttpResponse("Something went wrong!")

def edit_pie(request, id):
    context = {
        'pie' : models.get_pie_by_id(id)
    }
    return render(request, "pies_edit.html", context)

def edit_pie_update(request, id):
    models.edit_pie(id,request.POST)
    return redirect('/dashboard')

def pie_vote(request, id):
    logged_user = models.get_user_by_email(request.session['user_email'])

    context = {
        'pie' : models.get_pie_by_id(id),
        'user' : logged_user[0]
    }
    return render(request, "pies_vote.html", context)

def user_vote_pie(request):
    id_pie = request.POST['pie_id']
    logged_user = models.get_user_by_email(request.session['user_email'])
    models.vote_user_pie(request.POST, logged_user[0])
    return redirect('/pies/' + str(id_pie))

def remove_user_vote_pie(request):
    id_pie = request.POST['pie_id']
    logged_user = models.get_user_by_email(request.session['user_email'])
    models.remove_vote_user_pie(request.POST, logged_user[0])
    return redirect('/pies/' + str(id_pie))