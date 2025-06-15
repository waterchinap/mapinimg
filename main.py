import argparse
import os
from src.image_utils import get_image_dimensions, get_image_geolocation, overlay_map_on_image
from src.map_generator import generate_map_image
from PIL import Image # Required for saving the image, and potentially for other image ops if not handled by utils

def main():
    parser = argparse.ArgumentParser(description="Overlays a geolocation map onto an image.")
    parser.add_argument("image_path", help="Path to the input image.")
    parser.add_argument("--output_path", help="Path to save the output image. Defaults to 'output.jpg' in the input image's directory.")
    parser.add_argument("--zoom", type=int, default=10, help="Map zoom level. Defaults to 10.")

    args = parser.parse_args()

    # Get image dimensions
    original_dimensions = get_image_dimensions(args.image_path)
    if not original_dimensions:
        print(f"Could not get dimensions for image: {args.image_path}")
        return
    original_width, original_height = original_dimensions

    # Get image geolocation
    geolocation = get_image_geolocation(args.image_path)
    if not geolocation:
        print(f"Could not get geolocation for image: {args.image_path}. GPS EXIF data might be missing.")
        return
    lat, lon = geolocation

    # Calculate map dimensions (e.g., 1/3rd of the original image size)
    map_width = original_width // 3
    map_height = original_height // 3

    # Generate map image
    print(f"Generating map for Lat: {lat}, Lon: {lon} with zoom: {args.zoom}")
    map_pillow_image = generate_map_image(lat, lon, map_width, map_height, zoom=args.zoom)
    if not map_pillow_image:
        print("Could not generate map image.")
        return

    # Overlay map on the original image
    print("Overlaying map on image...")
    final_image = overlay_map_on_image(args.image_path, map_pillow_image)
    if not final_image:
        print("Could not overlay map on image.")
        return

    # Determine output path
    output_path = args.output_path
    if not output_path:
        # Default to output.jpg in the same directory as the input image
        input_dir = os.path.dirname(args.image_path)
        if not input_dir: # If image_path is just a filename without a directory
            input_dir = "."
        output_path = os.path.join(input_dir, "output.jpg")
    elif os.path.sep not in args.output_path and "/" not in args.output_path : # if it's just a filename
        input_dir = os.path.dirname(args.image_path)
        if not input_dir:
            input_dir = "."
        output_path = os.path.join(input_dir, args.output_path)

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)


    # Save the final image
    try:
        # Convert to RGB if saving as JPEG, as JPEG doesn't support alpha
        if output_path.lower().endswith(".jpg") or output_path.lower().endswith(".jpeg"):
            final_image = final_image.convert('RGB')
        final_image.save(output_path)
        print(f"Output image saved to: {output_path}")
    except Exception as e:
        print(f"Error saving final image: {e}")


if __name__ == "__main__":
    main()
