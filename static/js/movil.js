function convertir(latitude, longitude){
    latitude_sign  = 1;
    longitude_sign = 1;
    if(latitude < 0)
        latitude_sign = -1;
    if(longitude < 0)
        longitude_sign = -1;
    // Validations
    if(latitude > 90 || latitude < -90)
        throw "Latitude.degrees (-90 < d < 90) invalid: " + latitude;
    if(longitude > 180 || longitude < -180)
        throw "Longitude.degrees (-180 < d < 180) invalid: " + longitude;
    // Final calculations
    latitude_deg = Math.floor(Math.abs(latitude));
    latitude_min = Math.floor((Math.abs(latitude) - latitude_deg) * 60);
    latitude_sec = Math.ceil(((Math.abs(latitude) - latitude_deg) * 60 - latitude_min) * 60);
    latitude_dir  = (latitude_sign > 0) ? "N" : "S";
    longitude_deg = Math.floor(Math.abs(longitude));
    longitude_min = Math.floor((Math.abs(longitude) - longitude_deg) * 60);
    longitude_sec = Math.ceil(((Math.abs(longitude) - longitude_deg) * 60 - longitude_min) * 60);
    longitude_dir  = (longitude_sign > 0) ? "E" : "W";
    // Packing the results
    return {
        "latitude": {
            "degrees": Math.abs(latitude_deg),
            "minutes": latitude_min,
            "seconds": Math.round(latitude_sec),
            "dir": latitude_dir
        },
        "longitude": {
            "degrees": Math.abs(longitude_deg),
            "minutes": longitude_min,
            "seconds": Math.round(longitude_sec),
            "dir": longitude_dir
        }
    };
}
    
function ObtenerURL(x, y){
    var coordenadaX= x;
    var coordenadaY= y;
    var URL= "https://www.google.com.pe/maps/place/";
  	var respuesta = convertir(coordenadaX, coordenadaY);
  	var Latitud= respuesta["latitude"]["degrees"]+"\°"+respuesta["latitude"]["minutes"]+"\'"+respuesta["latitude"]["seconds"];
  	var Longitud= respuesta["longitude"]["degrees"]+"\°"+respuesta["longitude"]["minutes"]+"\'"+respuesta["longitude"]["seconds"]+"\""+respuesta["longitude"]["dir"];
  	URL = URL+Latitud+'\"'+respuesta["latitude"]["dir"]+'\+'+Longitud;
  	location.href=URL;
    //alert(URL);
};