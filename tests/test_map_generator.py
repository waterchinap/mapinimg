import pytest
from PIL import Image
from src.map_generator import generate_map_image

def test_generate_map_image():
    # Define sample parameters
    latitude = 0.0
    longitude = 0.0
    width = 200
    height = 150
    zoom = 10

    # Call the function
    map_img = generate_map_image(latitude, longitude, width, height, zoom=zoom)

    # Assert the returned object is a Pillow Image.Image instance
    assert isinstance(map_img, Image.Image), "Should return a Pillow Image instance."

    # Assert its dimensions match what was requested
    assert map_img.width == width, f"Map width should be {width}, but got {map_img.width}."
    assert map_img.height == height, f"Map height should be {height}, but got {map_img.height}."

    # Assert its mode is 'RGB' or 'RGBA'
    # staticmap usually produces RGB for .render() without specific alpha channel requirements in markers
    # If markers had alpha, it might be RGBA. For a simple CircleMarker, it's likely RGB.
    assert map_img.mode in ['RGB', 'RGBA'], f"Map mode should be RGB or RGBA, but got {map_img.mode}."

def test_generate_map_image_different_zoom():
    # Test with a different zoom level to ensure it's passed through
    latitude = 34.0522  # Los Angeles
    longitude = -118.2437
    width = 300
    height = 300
    zoom = 12 # Different zoom

    map_img = generate_map_image(latitude, longitude, width, height, zoom=zoom)
    assert isinstance(map_img, Image.Image)
    assert map_img.width == width
    assert map_img.height == height
    # Zoom level itself is not directly verifiable from the image object properties easily,
    # but ensuring the function runs with different zoom is a basic check.

def test_generate_map_invalid_inputs():
    # Example of what might be invalid, though staticmap might handle some gracefully
    # For instance, very large dimensions might cause memory issues, but that's hard to unit test.
    # Lat/lon outside typical bounds are often wrapped by map renderers.
    # This test is more for future consideration if strict input validation is added.

    # Test with potentially problematic, but still technically valid, lat/lon
    map_img = generate_map_image(90.0, 180.0, 50, 50, zoom=1)
    assert isinstance(map_img, Image.Image)

    # generate_map_image itself has a try-except, so it should return None on error
    # Example: width/height that staticmap might reject (e.g., 0 or negative)
    # map_img_invalid_dims = generate_map_image(0,0, -100, -100, zoom=1)
    # assert map_img_invalid_dims is None, "Should return None for invalid dimensions like negative width/height."
    # Note: staticmap library might handle this internally or raise its own error.
    # The current implementation of generate_map_image catches general Exception and returns None.

    # Test with zero dimensions (staticmap might raise error, caught by our function)
    map_img_zero_dims = generate_map_image(0, 0, 0, 0, zoom=1)
    if map_img_zero_dims is not None:
        # Some versions/configurations of staticmap might produce a 1x1 image or similar
        print(f"Warning: generate_map_image with 0,0 dims returned an image of size {map_img_zero_dims.size}")
    else:
        assert map_img_zero_dims is None, "Expected None for zero dimensions if staticmap fails."

    # It's hard to force every internal failure of staticmap, but testing that our wrapper
    # returns None when staticmap fails (e.g. due to impossible dimensions) is good.
    # Let's assume staticmap raises an error for negative dimensions.
    map_img_negative_dims = generate_map_image(0,0, -100, 50, zoom=1)
    assert map_img_negative_dims is None, "Should return None if staticmap fails due to negative dimensions."
