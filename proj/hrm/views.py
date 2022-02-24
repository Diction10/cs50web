from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from erp.models import *
from .forms import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    # check if the user is in accounting
    user = User.objects.get(username=request.user)
    department = user.department
    # redirect if not department
    if department != 'Human Resource':
        return render(request, 'erp/apology.html', {
            'department': department
        })
    else:
        return render(request, 'hrm/index.html')


# list of employees
@login_required
def employee_list(request):
    # query db
    users = User.objects.all()

    return render(request, 'hrm/employee_list.html', {
        'users': users,
        'count': users.count()
    })


# edit employee info
@login_required
def edit_employee_info(request, id):
    # get individual info of request.user
    user = User.objects.get(pk=id)

    # get the edit info form
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'department': user.department,
        'salary': user.salary,
        'sex': user.sex,
    }

    # prepopulate the form with the user's info
    form = editEmployeeInfo(initial=data)

    # query db
    # users = User.objects.all()

    if request.method == 'POST':

        reply = editEmployeeInfo(request.POST, instance=user)
        if reply.is_valid():
            reply.save()
        return HttpResponseRedirect(reverse("hrm:employee_list"))

    return render(request, 'hrm/edit.html', {
        # 'users': users,
        'form': form
    })
