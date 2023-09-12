import geopandas as gpd
from shapely.geometry import Point

lat = 48.393581
lon = -24.157794

# Carga el archivo GeoJSON con los límites de los continentes
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Definir un punto con las coordenadas que deseas verificar
coords = Point(lon, lat)  # Sustituye lon y lat con tus propias coordenadas

# Verifica si el punto está dentro de los límites de cualquier continente
inside_continent = False
for index, row in world.iterrows():
    if row['geometry'].contains(coords):
        inside_continent = True
        continent_name = row['continent']
        break

if inside_continent:
    print(f"Las coordenadas están dentro del continente {continent_name}.")
else:
    print("Las coordenadas no están dentro de ningún continente.")
