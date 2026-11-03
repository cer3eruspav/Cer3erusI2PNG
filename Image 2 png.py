"""
Image to PNG Converter
Part of the DAD (Drag and Drop) tool suite by CER3ERUS TECH.
Converts input images (.jpg, .jpeg, .webp, .bmp, .tiff, .ico, .jfif) into PNG files.
Preserves supported metadata and transparency where possible.
Automatically installs required libraries on first launch.
"""

import io
import os
import sys
import subprocess

REQUIRED_PACKAGES = ["Pillow"]

def ensure_dependencies():
    """Checks and automatically installs missing libraries on first run."""
    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__("PIL")
        except ImportError:
            missing.append(pkg)

    if missing:
        print("==================================================")
        print("    Image to PNG - Initial Setup                  ")
        print("==================================================")
        print(f"[*] Missing required libraries: {', '.join(missing)}")
        print("[*] Installing missing libraries via pip, please wait...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            print("[+] All dependencies installed successfully!\n")
        except Exception as e:
            print(f"[!] Warning: Failed to install dependencies automatically: {e}")
            print("[!] Please run 'pip install -r requirements.txt' manually.\n")

ensure_dependencies()

from PIL import Image, ImageCms

SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.webp', '.bmp', '.tiff', '.ico', '.jfif')


def convert_to_png(image_path: str) -> str | None:
    """
    Converts a single image to PNG without lossy re-encoding of the decoded pixels.
    Preserves supported metadata and converts profiled CMYK images to sRGB when possible.
    """
    try:
        with Image.open(image_path) as img:
            orig_width, orig_height = img.size
            orig_mode = img.mode

            # Preserve supported source metadata when writing the PNG.
            save_kwargs = {}
            source_icc_profile = img.info.get('icc_profile')
            if source_icc_profile:
                save_kwargs['icc_profile'] = source_icc_profile
            if 'dpi' in img.info:
                save_kwargs['dpi'] = img.info['dpi']
            if hasattr(img, 'getexif'):
                exif = img.getexif()
                if exif:
                    save_kwargs['exif'] = exif

            converted_img = img
            if orig_mode == 'CMYK':
                # Use the embedded CMYK profile to convert into standard sRGB when available.
                converted_img = img.convert('RGB')
                if source_icc_profile:
                    try:
                        source_profile = ImageCms.ImageCmsProfile(io.BytesIO(source_icc_profile))
                        srgb_profile = ImageCms.createProfile('sRGB')
                        converted_img = ImageCms.profileToProfile(
                            img,
                            source_profile,
                            srgb_profile,
                            outputMode='RGB'
                        )
                        save_kwargs['icc_profile'] = ImageCms.ImageCmsProfile(srgb_profile).tobytes()
                    except (ImageCms.PyCMSError, OSError, ValueError) as error:
                        print(f"[WARNING] Could not apply the embedded CMYK profile; using Pillow's RGB conversion: {error}")
                        save_kwargs.pop('icc_profile', None)
                else:
                    save_kwargs.pop('icc_profile', None)
                    print("[WARNING] CMYK input has no embedded ICC profile; color conversion uses Pillow's default conversion.")
            elif orig_mode == 'P':
                # Expand palette images to retain transparency in the PNG output.
                converted_img = img.convert('RGBA')
            elif orig_mode not in ('1', 'L', 'LA', 'RGB', 'RGBA', 'I', 'I;16'):
                has_alpha = 'A' in img.getbands() or 'transparency' in img.info
                converted_img = img.convert('RGBA' if has_alpha else 'RGB')

            output_path = save_to_unique_path(
                converted_img,
                image_path,
                ".png",
                "PNG",
                compress_level=6,
                **save_kwargs
            )

            print(f"[CREATED] {os.path.basename(output_path)} ({orig_width}x{orig_height} px, mode {converted_img.mode})")
            return output_path
    except Exception as e:
        print(f"[ERROR] Failed to convert {image_path}: {e}")
        return None


def save_to_unique_path(image, image_path: str, extension: str, image_format: str, **save_options) -> str:
    """Saves an image without replacing an existing file, adding numbered suffixes as needed."""
    base_dir = os.path.dirname(image_path)
    file_name = os.path.splitext(os.path.basename(image_path))[0]
    suffix = 0

    while True:
        numbered_name = file_name if suffix == 0 else f"{file_name} ({suffix})"
        output_path = os.path.join(base_dir, f"{numbered_name}{extension}")

        try:
            with open(output_path, "xb") as output_file:
                try:
                    image.save(output_file, format=image_format, **save_options)
                except Exception:
                    output_file.close()
                    os.remove(output_path)
                    raise
            return output_path
        except FileExistsError:
            suffix += 1


def verify_output_file(output_path: str, expected_format: str) -> bool:
    """Checks that the output exists and can be opened as the expected image format."""
    # Confirm the saved file exists and is readable before allowing source cleanup.
    if not os.path.isfile(output_path):
        print(f"[ERROR] Converted output was not found: {output_path}")
        return False

    try:
        with Image.open(output_path) as output_image:
            if output_image.format != expected_format:
                print(f"[ERROR] Unexpected output format for {output_path}: {output_image.format}")
                return False
            output_image.verify()
        return True
    except Exception as e:
        print(f"[ERROR] Converted output could not be verified: {output_path}: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Please drag and drop image file(s) onto this script or its shortcut.")
        return

    input_files = [
        f for f in sys.argv[1:]
        if os.path.exists(f) and f.lower().endswith(SUPPORTED_EXTENSIONS)
    ]

    if not input_files:
        print("[ERROR]: No supported image files found (or files are already PNG).")
        return

    for img_file in input_files:
        if img_file.lower().endswith(".png"):
            print(f"[SKIP] Already a PNG file: {os.path.basename(img_file)}")
            continue

        output_path = convert_to_png(img_file)
        if output_path and verify_output_file(output_path, "PNG"):
            try:
                # Remove source file only after the output has been verified
                os.remove(img_file)
                print(f"[CLEANUP] Deleted original file: {os.path.basename(img_file)}")
            except Exception as e:
                print(f"[WARNING] Could not delete original file {img_file}: {e}")
        else:
            print(f"[WARNING] Original file was kept because the converted output was not verified: {os.path.basename(img_file)}")

    print("\nProcessing finished. Review the messages above for conversion or cleanup warnings.")
    input("Press Enter to close this window...")


if __name__ == "__main__":
    main()
