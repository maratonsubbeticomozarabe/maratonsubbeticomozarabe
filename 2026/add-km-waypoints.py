import xml.etree.ElementTree as ET
import math

def haversine(lat1, lon1, lat2, lon2):
    """Calcula la distancia en kilómetros entre dos coordenadas geográficas."""
    R = 6371.0 # Radio de la Tierra en km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def add_km_waypoints(input_gpx, output_gpx):
    # Cargar el archivo GPX
    tree = ET.parse(input_gpx)
    root = tree.getroot()
    
    # Manejar los namespaces de GPX para no perder el formato original
    namespace = {'gpx': 'http://www.topografix.com/GPX/1/1'}
    ET.register_namespace('', namespace['gpx'])
    
    total_distance = 0.0
    next_km = 1
    prev_coords = None
    
    # Buscar todos los puntos del track (trkpt)
    for trkpt in root.findall('.//gpx:trkpt', namespace):
        lat = float(trkpt.get('lat'))
        lon = float(trkpt.get('lon'))
        
        if prev_coords is not None:
            # Calcular distancia desde el punto anterior y sumarla
            dist = haversine(prev_coords[0], prev_coords[1], lat, lon)
            total_distance += dist
            
            # Si hemos superado el siguiente múltiplo de 1 km
            while total_distance >= next_km:
                # Crear un nuevo elemento waypoint (wpt)
                wpt = ET.Element('wpt', {'lat': str(lat), 'lon': str(lon)})
                name = ET.SubElement(wpt, 'name')
                name.text = f'KM {next_km}'
                
                # Insertarlo justo al inicio del root (antes de los tracks)
                root.insert(1, wpt)
                next_km += 1
                
        prev_coords = (lat, lon)

    # Guardar el archivo modificado
    tree.write(output_gpx, encoding='utf-8', xml_declaration=True)
    print(f"¡Proceso completado! Se han añadido {next_km - 1} waypoints. Archivo guardado como: {output_gpx}")

# Ejecutar el script con tu archivo
add_km_waypoints('MSM50K-DONAMENCIA-ENCINASREALES.gpx', 'MSM50K_con_waypoints.gpx')