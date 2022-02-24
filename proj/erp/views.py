from math import fabs
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError

from django.contrib.auth.decorators import login_required
# from django.forms.models import model_to_dict
from .forms import *
from .models import *
import datetime
from sales import *
# from hrm.models import *


@login_required
def index(request):
    # Attempt to bring usser to home page or their department
    return render(request, 'erp/index.html')


# register view
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # print(obj.id)
            obj = form.save(commit=False)
            obj.save()

            # login(request, user)
            messages.success(
                request, f"Registration successful.")
            return redirect('index')
    else:
        form = RegistrationForm()

    return render(request, 'erp/register.html', {
        'form': form,
    })


# info set up
@login_required
def info(request):
    user_info = User.objects.get(username=request.user)

    # emp = User.objects.all()

    return render(request, 'erp/info.html', {
        'user_info': user_info,
    })


# edit info
@login_required
def edit_info(request):
    user_info = User.objects.get(username=request.user)
    # form = UpdateInfoForm()
    data = {
        'username': user_info.username,
        'first_name': user_info.first_name,
        'last_name': user_info.last_name,
        'email': user_info.email
    }
    form = UpdateInfoForm(initial=data)

    if request.method == 'POST':
        form = UpdateInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            # save to database
            form.save()
            messages.success(request, f'Your information has been updated!')
            # redirect to the new page
            return redirect('info')

    return render(request, 'erp/edit.html', {
        'form': form
    })


@login_required
def leave(request):
    # let's start writing the server side logic
    user_info = User.objects.get(username=request.user)

    if request.method == 'POST':
        # get the dates of the leave and convert them to date time
        leave_from = datetime.datetime.strptime(
            request.POST['departure'], '%Y-%m-%d').date()
        leave_arrival = datetime.datetime.strptime(
            request.POST['arrival'], '%Y-%m-%d').date()

        if leave_from > leave_arrival:
            messages.warning(request, f'Invalid Dat(s)')
        else:

            # get the days difference (leave duration)
            leave_duration = (leave_arrival - leave_from).days + 1

            # get users remaining leave days
            leave_days = user_info.leave_days

            # check if user has enough leave days remaining
            if leave_duration <= leave_days:
                leave_days = leave_days - leave_duration
                # save to database
                user_info = User.objects.update(leave_days=leave_days)

                messages.success(
                    request, f'Your Application has been approved!!!')
            else:
                messages.warning(request, f'Application unsuccessful, you have \
                                {leave_days} leave days left')

            return redirect('leave')

    return render(request, 'erp/leave.html', {
        'leave_days': user_info.leave_days
    })
