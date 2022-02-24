from django.urls import path

from . import views

app_name = 'sales'

urlpatterns = [
    path("index", views.index, name="index"),
    path("add_product", views.add_product, name="add_product"),
    path("download", views.download, name="download"),
    path("download_excel", views.download_excel, name="download_excel"),
    path("edit_product/<str:product>", views.edit_product, name="edit_product"),
    path("delete_product/<str:product>",
         views.delete_product, name="delete_product"),
]
