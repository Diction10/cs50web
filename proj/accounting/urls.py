from unicodedata import name
from django.urls import path

from . import views

app_name = 'accounting'

urlpatterns = [
    # path("index", views.index, name="index"),
    # path("index", views.index, name="index"),
    path('home', views.home, name='home'),
    path('billing', views.billing, name='billing'),
    path('invoice/<str:product>', views.show_invoice, name='invoice'),


    path('', views.index1),
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
]
