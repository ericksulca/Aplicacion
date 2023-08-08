from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import (ListAPIView)
from app.models import Presentacion

from app.serializers import PresentacionSerializer
class get_PresentacionProducto(ListAPIView):
    serializer_class = PresentacionSerializer
    def get_queryset(self,*args, **kwargs):
        print("############## PK in URL #################")
        kword = self.request.query_params.get('pk', '')
        #print(kword)
        oPresentaciones = Presentacion.objects.filter(estado = True)
        return oPresentaciones