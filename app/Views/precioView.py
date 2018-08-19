# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from ferreteria import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from app.fomularios.productoForm import *
import xlrd


def getPrecios(request):
    if request.method == 'GET':
        try:            
            jsonfinal = {}
            jsonfinal["precios"] = []
            oPrecio = Precio.objects.filter(estado = True)      
            for precio in oPrecio:
                preciojson = {}
                preciojson["id"] = precio.id
                preciojson["nombre"] = precio.nombre
                jsonfinal['precios'].append(preciojson)
            return HttpResponse(json.dumps(jsonfinal), content_type="application/json")
        except:
            return HttpResponse(json.dumps({'exito':0}), content_type="application/json")

def IngresarPrecios(request):
	book = xlrd.open_workbook("/home/mouse/ferreteria/ferreteria/media/Libro.xls")
	sheet = book.sheet_by_name("Hoja1")
	for r in range(1, sheet.nrows):
		a = sheet.cell(r,1).value
		b = sheet.cell(r,2).value
		c = sheet.cell(r,3).value
		print(a)
		oPrecio = Precio()
		oPrecio.nombre = a
		#oPrecio.save()
		print(b)
	return HttpResponse(json.dumps({'exito':0}), content_type="application/json")
