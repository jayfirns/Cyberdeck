# Gemini Workspace - Freenove Computer Case Kit

This directory contains the code and resources for the Freenove Computer Case Kit for Raspberry Pi.

## Project Overview

This project is a Python application that runs on a Raspberry Pi equipped with the Freenove Computer Case Kit. The application monitors the Raspberry Pi's system vitals, including CPU usage, memory usage, disk usage, and temperature. It also controls the kit's hardware components, such as an OLED display, addressable LEDs, and cooling fans.

The main application, `application.py`, runs in a loop to collect system data and update the OLED display with real-time information. It also manages the cooling fan based on the CPU temperature. The `generate_service.py` script is provided to set up the main application as a systemd service, ensuring it runs automatically on boot.

The project utilizes the following key libraries:
- **`psutil`**: For gathering system information like CPU, memory, and disk usage.
- **`smbus`**: For I2C communication with the expansion board.
- **`luma.oled`**: For controlling the OLED display.
- **`PIL (Pillow)`**: For image manipulation and display on the OLED screen.
- **`picamera2`**: For camera functionalities.

## Development Environment

The `cyberdeck` branch is considered the gold standard and will not be directly developed upon. All development and modifications to this project will occur on separate feature branches, which will then be merged into `cyberdeck` after review and testing. The current goal is to improve and enhance the existing framework and expand upon the functionality defined in the code.

## Building and Running

### Prerequisites

- A Raspberry Pi with the Freenove Computer Case Kit.
- Python 3.
- The required Python libraries installed. You can likely install them using pip:
  ```bash
  pip install psutil smbus luma.oled Pillow picamera2
  ```

### Running the Application

The main application can be run directly from the `Code` directory:

```bash
cd Code
python3 application.py
```

### Installing as a Service

To have the application start automatically on boot, you can use the `generate_service.py` script. This will create and enable a systemd service.

```bash
cd Code
sudo python3 generate_service.py
```

This will perform the following actions:
1.  Create a `my_app_running.service` file in `/etc/systemd/system/`.
2.  Reload the systemd daemon.
3.  Enable the service to start on boot.
4.  Start the service immediately.

You can check the status of the service using:

```bash
sudo systemctl status my_app_running.service
```

## Development Conventions

The code is written in Python and follows standard Python conventions.

- The `application.py` script is the main entry point and contains the monitoring and control loop.
- Hardware interactions are abstracted into classes:
    - `OLED` in `oled.py` for the OLED display.
    - `Expansion` in `expansion.py` for the expansion board (LEDs, fan, temperature sensor).
    - `Camera` in `camera.py` for the camera.
- The `generate_service.py` script is used for deployment and should not need modification for typical use.

The project is structured to be modular, with clear separation of concerns between the main application logic and the hardware control modules.
