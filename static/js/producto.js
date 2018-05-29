$(document).ready(function(){
	CantidadPresentaciones =0;
});

function AgregarUnidad(){
	 
}
function ListarPrecios(){
	alert(CantidadPresentaciones);
	$.ajax({        
        type: "GET",
            url: strRootUrl+"Precios/getPrecios/",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function (response) {  
                var oPrecios = response.precios;
                for (var i = 0; i < oPrecios.length; i++) {
                	alert(oPrecios[i].nombre);
            };
        },
        error: function (result) {
            alert('ERROR.... en ' + result.status + '... ' + result.statusText);
        }
    });
}

function cantTipoPrecios(){
	//alert(CantidadPresentaciones);
	
}
function AgregarContenido(){
	CantidadPresentaciones +=1;
	var cmbPresentacionId  = $("#cmbPresentacion").val();
	//$("#miCombo option:selected").html();
	var cmbPresentacionVal  = $("#cmbPresentacion option:selected").text();
	var cantPresentacion = $("#cantPresentacion").val();
	//var valPrecios = [];
	//cantTP = cantTipoPrecios();
	//var valPrecio1       = $("#1Precio").val();
	//var valPrecio2       = $("#2Precio").val();
	//var valPrecio2       = $("#3Precio").val();
	campo = '</div>Tipo de Unidad</br><select class="form-control" id="cmbPresentacion'+CantidadPresentaciones+'" required="""></option><option value="'+cmbPresentacionId+'">'+cmbPresentacionVal+'</option></select>	<br /> Cantidad de Presenttación<input type="number" name="cantPresentacion'+CantidadPresentaciones+'" id="cantPresentacion'+CantidadPresentaciones+'" required="" class="form-control" value="'+cantPresentacion+'"></br>';

	$.ajax({        
        type: "GET",
            url: strRootUrl+"Precios/getPrecios/",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function (response) {  
                var oPrecios = response.precios;
                htmlPrecios = "";
                for (var i = 0; i < oPrecios.length; i++) {
                	idImput = oPrecios[i].id+"PrecioPresentacion";
                	idImputModal = "#"+oPrecios[i].id+"Precio";
                	nombreLabel = oPrecios[i].nombre;
                	htmlPrecios+= nombreLabel+'<br/> <input type="number" name="'+idImput+'" id="'+idImput+'" class="form-control" value="'+$(idImputModal).val()+'"><br />';
            	};
            	campo+= ""+htmlPrecios;
				campo+= "</div>";
				$("#OtrasUnidades").append(campo);
        },
        error: function (result) {
            alert('ERROR.... en ' + result.status + '... ' + result.statusText);
        }
    });
	
}
 