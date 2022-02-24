from django.http.response import Http404
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from itsdangerous import exc
from xlwt.Column import Column
from .forms import *
from .models import *
from django.urls import reverse
from django.forms.models import model_to_dict
import csv
from django.http import JsonResponse
from django.core import serializers
import json
import xlwt
import datetime
from erp.models import *
from django.contrib.auth.decorators import login_required
# list of available product


@login_required
def index(request):
    # check if the user is in accounting
    user = User.objects.get(username=request.user)
    department = user.department
    # redirect if not department
    if department != 'Sales':
        return render(request, 'erp/apology.html', {
            'department': department
        })
    else:
        # get all the items avalable
        products = Product.objects.all()
        return render(request, 'sales/product_list.html', {
            'products': products
        })


# add product
@login_required
def add_product(request):

    form = addInventory()

    if request.method == 'POST':

        reply = addInventory(request.POST)
        product_typed = reply.data['name'].lower()

        try:
            # query db for products
            product = Product.objects.get(name=product_typed)
            # check if product already exists
            if product_typed == str(product):
                messages.warning(
                    request, 'This product has already been added please edit it')
                print('This product has already been added please edit it')

        except Exception as error:
            if reply.is_valid():
                obj = reply.save(commit=False)
                obj.user = request.user
                obj.save()
                messages.success(
                    request, 'Product has been added successfully!')

        return HttpResponseRedirect(reverse("sales:index"))

    return render(request, 'sales/index.html', {
        'form': form
    })


# edit individual product
@login_required
def edit_product(request, product):
    product = Product.objects.get(name=product)
    # get the pre-populated form
    form = addInventory(initial=model_to_dict(product))
    if request.method == 'POST':
        f = addInventory(request.POST, instance=product)

        if f.is_valid():
            f.save()
            messages.success(
                request, f'{product} has been edited successfully!')
        return HttpResponseRedirect(reverse("sales:index"))

    return render(request, 'sales/index.html', {
        'form': form
    })


@ login_required
def delete_product(request, product):
    # query db to delete product
    product = Product.objects.get(name=product)
    product.delete()
    messages.success(
        request, f'{product} has been added successfully!')
    return HttpResponseRedirect(reverse("sales:index"))


# download files in differnet format
@ login_required
def download(request):
    # query db for product inventr
    products = Product.objects.all()

    # set response
    response = HttpResponse(content_type='text/csv')

    # set file
    response['Content-Disposition'] = 'attachment; filename=Folakayo+' + '.txt'

    # sset writer
    writer = csv.writer(response)

    # print(dir(writer))
    # write the rows of the files
    writer.writerow(['S/N', 'Name', 'Price', 'Quantity'])

    # loop through the data to fill in the rows dynamically
    for product in products:
        writer.writerow([product.id, product.name,
                        product.price, product.quantity])

    return response


# to download in excel format
@ login_required
def download_excel(request):
    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')

    # decide file name
    response['Content-Disposition'] = 'attachment; filename="Product_List.xls"'

    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    # adding sheet
    ws = wb.add_sheet("sheet1")

    # Sheet header, first row, where the row should sart
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    # column header names, you can use your own headers here
    columns = ['S/N', 'Name', 'Price($)', 'Quantity', ]

    # write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # get data from database
    data = Product.objects.all()
    for index, my_row in enumerate(data):
        row_num = row_num + 1

        ws.write(row_num, 0, index + 1, font_style)
        ws.write(row_num, 1, my_row.name, font_style)
        ws.write(row_num, 2, "{:.2f}".format(my_row.price), font_style)
        ws.write(row_num, 3, my_row.quantity, font_style)

    wb.save(response)
    return response
