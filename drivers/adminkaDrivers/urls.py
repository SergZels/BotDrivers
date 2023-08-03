from django.urls import path

from . import views

urlpatterns = [
    path("", views.index1, name="index1"),
    path("site/", views.index2, name="index2"),
    path("api/", views.PublicationsList.as_view()),
    path("drivers/", views.DriversList.as_view()),
    path("driveridbytelid/", views.DriverIdByTelId.as_view()),
    path("codidbycode/", views.CodeIdByCode.as_view()),
    path("driver/<int:pk>/", views.DrivByid.as_view()),

]