from django.http import HttpResponse, JsonResponse
from .models import Publications, Driver, Cod
from django.shortcuts import render
from .serializers import PublicationsSerializers, DriversSerializers, CodsSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

class DrivByid(generics.UpdateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriversSerializers

class PublicationsList(generics.ListCreateAPIView):
    queryset = Publications.objects.all()
    serializer_class = PublicationsSerializers

class DriverIdByTelId(generics.ListCreateAPIView):
    serializer_class =DriversSerializers
    def get_queryset(self):
        queryset = Driver.objects.all()
        id = self.request.query_params.get('telegramId')
        if id is not None:
            queryset = queryset.filter(telegramId=id)
        return queryset

class CodeIdByCode(generics.ListCreateAPIView):
    serializer_class = CodsSerializer
    def get_queryset(self):
        queryset = Cod.objects.all()
        cod = self.request.query_params.get('cod')
        if cod is not None:
            queryset = queryset.filter(cod=cod)
        return queryset

# class DriverIdByTelId(APIView):
#     def get(self, request):
#         telegram_id = request.query_params.get("telegramId", "")
#         try:
#             driver = Driver.objects.get(telegramId=telegram_id)
#             data = {
#                 "id": driver.id,
#
#                 # Додайте інші поля з моделі `Driver`, які ви хочете повернути
#             }
#             return Response(data)
#         except Driver.DoesNotExist:
#             return Response({"error": "Driver not found"}, status=404)
#
#     def post(self,request):
#         id = request.query_params.get("telegramId", "")
#         ret = Driver.objects.get(telegramId = id)
#         return Response({"id": ret})

class DriversList(APIView):
    def get(self,request):
        name = request.query_params.get("name", "")
        ret = Driver.objects.get(name=name)
        return Response({"res": f'Data - {ret.name} {ret.text} {ret.telegramId} '})

    def post(self,request):
        ret = Driver.objects.get(pk=4)
        print(ret.name, ret.telegramId, request.data)
        return Response({"res": 'Hello post'})

def index1(request):
    db = Publications.objects.get(pk=1)
    res = db
    return HttpResponse(f"Driver {res}")

def index2(request):
    db = Publications.objects.filter(PublicationsAllowed=True)

    return render(request,"adminkaDrivers/index2.html", {'db':db, 'title':"List","pageName":"Hello list"})
