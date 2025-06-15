from PIL import Image

def get_image_dimensions(image_path):
    """
    Opens an image and returns its width and height.

    Args:
        image_path (str): The path to the image file.

    Returns:
        tuple: A tuple containing the width and height of the image (width, height),
               or None if the image cannot be opened.
    """
    try:
        with Image.open(image_path) as img:
            return img.size
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None
    except Exception as e:
        print(f"Error opening or reading image: {e}")
        return None

def get_image_geolocation(image_path):
    """
    Extracts GPS latitude and longitude from an image's EXIF data.

    Args:
        image_path (str): The path to the image file.

    Returns:
        tuple: A tuple containing the latitude and longitude in decimal degrees (lat, lon),
               or None if GPS data is not found or an error occurs.
    """
    try:
        import exifread
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)

            if not tags:
                print(f"No EXIF tags found in {image_path}")
                return None

            gps_latitude = tags.get('GPS GPSLatitude')
            gps_latitude_ref = tags.get('GPS GPSLatitudeRef')
            gps_longitude = tags.get('GPS GPSLongitude')
            gps_longitude_ref = tags.get('GPS GPSLongitudeRef')

            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                lat = _convert_to_degrees(gps_latitude.values)
                if gps_latitude_ref.values[0] != 'N':
                    lat = -lat

                lon = _convert_to_degrees(gps_longitude.values)
                if gps_longitude_ref.values[0] != 'E':
                    lon = -lon
                return (lat, lon)
            else:
                # print(f"GPS EXIF data not found in {image_path}")
                return None
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None
    except Exception as e:
        print(f"Error processing EXIF data: {e}")
        return None

def _convert_to_degrees(values):
    """
    Helper function to convert GPS exif data (degrees, minutes, seconds) to decimal degrees.
    """
    d = float(values[0].num) / float(values[0].den if values[0].den != 0 else 1)
    m = float(values[1].num) / float(values[1].den if values[1].den != 0 else 1)
    s = float(values[2].num) / float(values[2].den if values[2].den != 0 else 1)
    return d + (m / 60.0) + (s / 3600.0)


def overlay_map_on_image(original_image_path, map_image_pillow_object):
    """
    Overlays a map image onto an original image at the bottom-left corner with 50% transparency.

    Args:
        original_image_path (str): Path to the original image file.
        map_image_pillow_object (PIL.Image.Image): The map image (Pillow Image object).

    Returns:
        PIL.Image.Image: The modified original image with the map overlay,
                         or None if an error occurs.
    """
    try:
        original_image = Image.open(original_image_path).convert('RGBA')
        map_image = map_image_pillow_object.convert('RGBA')

        # Adjust transparency of the map image
        alpha = map_image.split()[3]
        alpha = alpha.point(lambda p: p * 0.5)  # 50% opacity
        map_image.putalpha(alpha)

        # Define position for the map (bottom-left corner)
        position = (0, original_image.height - map_image.height)

        # Paste the map onto the original image
        original_image.paste(map_image, position, map_image)  # Use map_image as mask for transparency

        return original_image
    except FileNotFoundError:
        print(f"Error: Original image file not found at {original_image_path}")
        return None
    except Exception as e:
        print(f"Error overlaying map on image: {e}")
        return None
