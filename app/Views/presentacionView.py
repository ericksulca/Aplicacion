from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import (ListAPIView)
from app.models import Presentacion, Producto_presentacions

from app.serializers import Producto_presentacionsSerializer
class get_PresentacionProducto(ListAPIView):
    serializer_class = Producto_presentacionsSerializer
    def get_queryset(self,*args, **kwargs):
        kword = self.request.query_params.get('pk', '')
        oPresentaciones = Producto_presentacions.objects.filter(estado = True,producto=kword)
        return oPresentaciones