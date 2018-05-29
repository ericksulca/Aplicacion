$(document).ready(function(){
	lstIniFin = [];
    lstTareas = [];
    lstValores = [];
    lstDependencias = [];
    lstValoresDependencias = [];

	$('#Tabla').hide();
	var Cantidad = 0;
	 
	//$("select[name=seclect1]").change(function(){
    //    alert("Hola!");
    //});
    //$("select[name=seclect1]").bind("change", function(){
	//alert("hola");
	//});
	$("select[name=seclect1]").on('change', function() {
		alert('El valor es: '); 
	});
	 
});

function AgregarDependencia(numeroLetra){
	var letra = String.fromCharCode(numeroLetra);
	var ordenItem = numeroLetra-65;
	nextCombo = lstDependencias[ordenItem];
	nextCombo++;
	lstDependencias[numeroLetra-65]=nextCombo;
	//var idCombo = letra+nextCombo;
	var idCombo = letra;
	//campo = '<select name="seclect1" id="'+idCombo+'"><option value="" ></option>';
	campo = '<select name="seclect1" id="seclect1" class="selectpicker" ><option value="" ></option>';
	var y = lstTareas;
	var removeItem = letra;
	y = jQuery.grep(y, function(value) {
	  return value != removeItem;
	});
	$.each(y, function (ind, elem) { 
		campo+='<option value="'+elem+'">'+elem+'</option>';
	});

	campo+='</select>';
	$("#depen"+letra).append(campo);
	// 			evento change selct's
	$("select[name=seclect1]").on('change', function() {
		//ObtenerDependencia(this,ordenItem); 
	});
}
function CrearTareas(){
	$('#formulario').hide();
	$('#Tabla').show();
	Cantidad = $(cantidad).val();
	var n = Cantidad;
	Inicial = 65;
	for (i = 0; i < n; i++) { 
		var item = 1;
		var letra = String.fromCharCode(Inicial+i);
		var letraNumerico=Inicial+i;
	    lstTareas.push(letra);
	    //alert(ArrTareas["letra"]);
	    item+=i;
	    if (i!=0) {
	    	var nuevaFila="<tr><td>"+item+"</td><td>"+letra+"</td><td><input id='input"+letra+"' type='number' class='form-control' /><td><div id='depen"+letra+"'></div> <a href='#' onclick='AgregarDependencia("+letraNumerico+");'>+</a> </td></tr>";
			$("#table").append(nuevaFila);
	    }else{
	    	var nuevaFila="<tr><td>"+item+"</td><td>"+letra+"</td><td><input id='input"+letra+"' type='number' class='form-control' /><td></td></tr>";
			$("#table").append(nuevaFila);
	    }
	}
	$.each(lstTareas, function (ind, elem) { 
	    lstDependencias.push(0);
	});
}
function Calcular(){
	ObtenerValores();
	ObtenerDependencias();
}
function ObtenerValores(){
	var n = Cantidad;
	Inicial = 65;
	for (i = 0; i < n; i++) { 
		var letra = String.fromCharCode(Inicial+i);
		var valorTarea=document.getElementById("input"+letra).value;
		lstValores.push(valorTarea);
	}
	//console.log(lstValores);
}
function ObtenerDependencia(obj,nItem){
	alert($(obj).attr("value"));
	//objDependencia = [];
	//objDependencia.orden = nItem;
	//objDependencia.tarea = $(obj).attr("value");
	//lstValoresDependencias.push(objDependencia);
}

function ObtenerDependencias(){
	var Combos=document.getElementsByName("seclect1");
	j = 0;
	$.each(lstDependencias, function (index, item) { 
		console.log(index+" - "+item);
	    for (var i = 0; i < item; i++) {
	    	var porNombre=document.getElementsByName("seclect1")[j].value;
			objDependencia = [];
			objDependencia.tarea = index;
			objDependencia.dependencia = porNombre;
			lstValoresDependencias.push(objDependencia);
			j++;
	    }
	});
	//console.log(lstValoresDependencias);
	mayor = parseInt(lstValores[0]);
	objInicioFinal = [];
	objInicioFinal.inicio = 0;
	objInicioFinal.final = mayor;
	lstIniFin.push([objInicioFinal.inicio,objInicioFinal.final]);
	var anterior = 0;
	var valoresDependencia = [];
	anteriorValorDep = 0;
	cantidaDependencias = lstValoresDependencias.length;
	$.each(lstValoresDependencias, function (index, item) { 
		depLetra = item.dependencia;
		numeroLetra1 = depLetra.charCodeAt(0)-65;
		console.log(numeroLetra1);
		if (item.tarea==anterior) {
			numero1 = anteriorValorDep;
			numero2 = parseInt(lstValores[numeroLetra1]);
			if(numero1>numero2){
				mayor = numero1;
			}else{
				mayor = numero2;
			}
			objInicioFinal = [];
			objInicioFinal.inicio = parseInt(mayor);
			objInicioFinal.final = parseInt(mayor) + parseInt(lstValores[item.tarea]);
			mayor = objInicioFinal.final;
			lstIniFin.push([objInicioFinal.inicio,objInicioFinal.final]);
			valoresDependencia = [];
			anteriorValorDep = objInicioFinal.final;
		}else{
			objInicioFinal = [];
			objInicioFinal.inicio = parseInt(lstValores[numeroLetra1]);
			objInicioFinal.final = objInicioFinal.inicio + parseInt(lstValores[item.tarea]);

			if (index+1<cantidaDependencias) {
				if (item.tarea!=lstValoresDependencias[index+1].tarea) {
					if (objInicioFinal.final>anteriorValorDep) {
						anteriorValorDep = objInicioFinal.final;
					}
					lstIniFin.push([objInicioFinal.inicio,objInicioFinal.final]);
				}
			}
			mayor = objInicioFinal.final;
			valoresDependencia = [];
		}
		anterior = item.tarea;
	});
	console.log(lstIniFin);

	///////////////////////////
	///
	///
	Highcharts.chart('container', {

    chart: {
        type: 'columnrange',
        inverted: true
    },

    title: {
        text: 'Tareas del proyecto'
    },

    subtitle: {
        text: 'Despliegue de tareas'
    },

    xAxis: {
        categories: lstTareas
    },

    yAxis: {
        title: {
            text: 'días'
        }
    },

    tooltip: {
        valueSuffix: ' días'
    },

    plotOptions: {
        columnrange: {
            dataLabels: {
                enabled: true,
                formatter: function () {
                    return this.y + ' días';
                }
            }
        }
    },

    legend: {
        enabled: false
    },

    series: [{
        name: 'Tiempo de Tareas',
        data: lstIniFin
    }]

});
}