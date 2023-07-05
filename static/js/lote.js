$(document).ready(function() {
  $('#id_Total').text("0.00");
  $('#bt_add').click(function() {
    agregar();
  });
  $('#bt_del').click(function() {
    eliminar(id_fila_selected);
  });
  $('#bt_delall').click(function() {
    eliminarTodasFilas();
  });

  $('#bt_GenerarLote').click(function() {
    InsertarLote();
  });

  $("#precioUnitario").change(function() {
    //alert($(this).val());
    //alert("hola");
    //$('#valor2').val($(this).val());
  });

});

function reset_values() {
  $('#inpt-producto').val('');
  $('#codigo').val('');
  $('#precio').val('');
  $('#cantidad').val('');
}

var TotalVenta = 0;
var cont = 0;
var id_fila_selected = [];

function agregar() {
  cont++;
  Producto = $('#inpt-producto').val();
  codigo = $('#codigo').val();
  cantidad = $('#cantidad').val();
  error = "";
  if (Producto == '') {
    error = 1;
  }

  if (cantidad == '') {
    error = 2;
  }
  if (error == "") {
    var fila = '<tr class="selected" id="fila' + cont +
      '" onclick="seleccionar(this.id);"><td>' + cont + '</td><td>' + cantidad +
      '</td><td>' + codigo + '</td><td>' + Producto +
      '</td></tr>';
    $('#tabla').append(fila);


    //$('#id_Total').text("S/. "+TotalVenta);
    reset_values();
    reordenar();
  } else {
    switch (error) {
      case 1:
        alert("Seleccione un producto válido!");
        $("#inpt-producto").focus();
        break;
      case 2:
        alert("Ingrese una cantidad");
        $("#cantidad").focus();
        break;

    }
  }
   $( "#cantidad" ).focus();
}

function seleccionar(id_fila) {
  if ($('#' + id_fila).hasClass('seleccionada')) {
    $('#' + id_fila).removeClass('seleccionada');
  } else {
    $('#' + id_fila).addClass('seleccionada');
  }
  //2702id_fila_selected=id_fila;
  id_fila_selected.push(id_fila);
}

function eliminar(id_fila) {
  /*$('#'+id_fila).remove();
  reordenar();*/
  ValorRestar = 0;
  for (var i = 0; i < id_fila.length; i++) {
    $('#' + id_fila[i]).children("td").each(function(index2) {
      switch (index2) {
        case 5:
          ValorRestar = parseFloat($(this).text()).toFixed(2);
          break;
      }
    });
    //TotalVenta = TotalVenta - ValorRestar
    //$('#id_Total').text("S/. "+TotalVenta);
    $('#' + id_fila[i]).remove();
  }
  reordenar();
}

function reordenar() {
  var num = 1;
  $('#tabla tbody tr').each(function() {
    $(this).find('td').eq(0).text(num);
    num++;
  });
}


function eliminarTodasFilas() {
  $('#id_Total').text("0.00");
  $('#tabla tbody tr').each(function() {
    $(this).remove();
  });

}

function InsertarLote() {
  var num = 1;
  productos = [];
  contador = 0;
  $("#tabla tbody tr").each(function(index) {
    $(this).children("td").each(function(index2) {
      producto = [];
      switch (index2) {
        case 1:
          cantidad = $(this).text();
          break;
        case 2:
          codigoProducto = $(this).text();
          break;
      }
    });
    contador = 1;
    productos.push([cantidad, codigoProducto]);
  });
  console.log(productos);
  if (contador == 1) {
    var datos = {
      productos: productos
    };
    var sendData = JSON.stringify(datos);
    $.ajax({
      type: "POST",
      dataType: "json",
      url: ".",
      data: sendData,
      contentType: "application/json; charset=utf-8",
      async: false,
      cache: false,
      CrossDomain: true,

      success: function(result) {
        var id_venta = result["id_venta"];
        alert('Lote registrado con éxito!');
        location.reload(true);
        num = 0;
      }
    });
  } else {
    alert("No registró ningún producto");
  }
}
