from staticmap import StaticMap, IconMarker, CircleMarker # Added CircleMarker for flexibility
from PIL import Image

def generate_map_image(latitude, longitude, width, height, zoom=10):
    """
    Generates a map image with a marker at the given latitude and longitude.

    Args:
        latitude (float): Latitude for the marker.
        longitude (float): Longitude for the marker.
        width (int): Width of the map image.
        height (int): Height of the map image.
        zoom (int, optional): Zoom level of the map. Defaults to 10.

    Returns:
        PIL.Image.Image: The generated map image as a Pillow Image object,
                         or None if an error occurs.
    """
    try:
        m = StaticMap(width, height)
        # Using CircleMarker as a default, IconMarker would require an icon image path
        marker = CircleMarker((longitude, latitude), 'red', 10) # (lon, lat), color, diameter
        m.add_marker(marker)
        image = m.render(zoom=zoom)
        return image
    except Exception as e:
        print(f"Error generating map image: {e}")
        return None
