from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from erp.models import *
from .forms import *
from sales.models import Product

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa


@login_required
def home(request):
    # check if the user is in accounting
    user = User.objects.get(username=request.user)
    department = user.department

    # redirect if not department
    if department != 'Accounting':
        return render(request, 'erp/apology.html', {
            'department': department
        })
    else:
        return render(request, 'accounting/index1.html')


# generate a bill
@login_required
def billing(request):
    form = BillingForm()

    if request.method == 'POST':
        form = BillingForm(request.POST)
        # get product id from form
        product_id = form.data['product']
        product_quantity_request = int(form.data['quantity'])

        # query sales db for information on product
        product = Product.objects.get(id=product_id)

        product_price = product.price
        product_quantity = product.quantity

        # check if quantity requested is more than quantity available
        if product_quantity_request > product_quantity:

            messages.warning(
                request, f'We only have {product_quantity} quantities of {product} available! ')
            form = BillingForm(request.POST)
        else:
            total_amount = product_price * product_quantity_request

            if form.is_valid():
                obj = form.save(commit=False)
                obj.price = product_price
                obj.total_amount = total_amount
                obj.save()

                # update Product table in sales database
                Product.objects.update(
                    quantity=product_quantity-product_quantity_request)
                # messages.success(
                #     request, 'Bill has been generated successfully!')

                return redirect('accounting:invoice', product)

    return render(request, 'accounting/billing.html', {
        'form': form,
    })


@login_required
def show_invoice(request, product):

    # # query db for the bill
    bill = Billing.objects.filter().last()
    # return HttpResponse(f'This is the invoice of {bill.id}')

    return render(request, 'accounting/invoice.html', {
        'product': bill.product,
        'quantity': bill.quantity,
        'price': bill.price,
        'total': bill.total_amount,
        'date': bill.transaction_date
    })


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# Opens up page as PDF


class ViewPDF(View):
    def get(self, request, *args, **kwargs):

        pdf = render_to_pdf('accounting/invoice.html')
        return HttpResponse(pdf, content_type='application/pdf')


# Automaticly downloads to PDF file
class DownloadPDF(View):
    def get(self, request, *args, **kwargs):

        pdf = render_to_pdf('accounting/pdf_template.html')

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice.pdf"
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response


def index1(request):
    context = {}
    return render(request, 'accounting/index.html', context)
