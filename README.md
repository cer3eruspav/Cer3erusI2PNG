# Image to PNG Converter

A drag-and-drop image converter that saves supported images as PNG. Part of the **DAD (Drag and Drop)** tool suite by **CER3ERUS TECH**.

Convert images in `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tiff`, `.ico`, or `.jfif` formats into `.png` files.

---

## Features

- **Drag & Drop Simplicity**: Drag and drop one or multiple images onto `Cer3erusI2PNG.bat` or its desktop shortcut to begin instant conversion.
- **PNG Output**: PNG uses lossless compression for the pixel data written to the output file.
- **Metadata and Transparency**: Preserves supported ICC profile, DPI, EXIF metadata, and transparency where possible. CMYK images with a usable embedded ICC profile are converted to sRGB; otherwise Pillow's default conversion is used with a warning.
- **Duplicate-Safe Output Names**: Never replaces an existing output file. If `photo.png` already exists, the next result is saved as `photo (1).png`, then `photo (2).png`, and so on.
- **Verified Source Cleanup**: Deletes the original only after the output file is found and verified as a readable `.png`. If verification fails, the original is kept. Back it up first if you need to keep it regardless.
- **Already-PNG Inputs**: Skips images that are already in `.png` format.

> PNG's lossless compression does not restore detail lost in a lossy source such as JPEG or WebP. Color-mode conversion (for example, CMYK to RGB) can also change pixel values; results depend on the source image and its embedded profile.

---

## Requirements

- **Operating System**: Windows 10 / Windows 11
- **Python**: Python 3.10+
- **Library**: `Pillow`

Install dependency:
```powershell
pip install -r requirements.txt
```

---

## Setup

1. Keep the downloaded program files together in the folder where you want to use the converter.
2. Double-click `Shortcut Creator for Distribution.vbs`. It creates `Cer3erusI2PNG.lnk` beside the launcher and applies the included `.ico` file.
3. Copy `Cer3erusI2PNG.lnk` to your Desktop if you want a convenient drop target. If you move the program folder, run the shortcut creator again and replace any old shortcut.

## How to Use

1. Drag and drop one or more supported image files onto `Cer3erusI2PNG.lnk` or `Cer3erusI2PNG.bat`.
2. The `.png` file will be generated in the same directory as the original image.
3. If an output with that name already exists, a numbered filename is used. The source image is removed only after the new `.png` is found and verified as readable.

> **Original File Notice**: The source image is deleted after a successful conversion. If you wish to retain the original source format, create a backup copy beforehand.

---
---

## Author & Organization

- **Organization**: CER3ERUS TECH
- **Project**: DAD (Drag and Drop Tool Suite)

## Voluntary Support

If you find this project useful, you may optionally support its development with TUSD on the TRON network. Support is entirely voluntary and does not provide additional features or change the project's usage terms.

**TUSD (TRON) address:** `TQSPCZAYQGe5pAbMMLtoDpS2gyQMWvXuQW`

![TUSD on TRON donation QR code](TUSD-TRON-QR.png)
