# AOS Device Loader (aosdl.py)

## Overview
The `aosdl.py` script automates the process of connecting to multiple devices via SSH, identifying their platform family, and downloading the appropriate AOS images to the devices' flash storage.

## Features
- Connects to devices using SSH.
- Identifies platform family based on shell prompt.
- Downloads AOS images based on platform family.
- Supports multiple devices with customizable credentials.

## Requirements
- Python 3.x
- `paramiko` library

## Installation
1. Ensure Python 3.x is installed on your system.
2. Install the `paramiko` library using pip:
   ```bash
   pip install paramiko
   ```

## Usage
1. Run the script:
   ```bash
   python3 aosdl.py
   ```
2. Follow the prompts to enter AOS version information and device details.
3. The script will connect to each device, identify its platform family, and download the appropriate images.

## Configuration
### Image Mapping
The script uses a predefined mapping of platform families to image files. You can modify the `image_map` dictionary in the script to add or update mappings.

### Constants
- `base_ip`: Base IP of your software repo for downloading images.

## Error Handling
The script handles errors such as:
- Connection failures.
- Unknown or missing platform family.

