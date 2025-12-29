# Gemini Workspace - Freenove Computer Case Kit

This directory contains the code and resources for the Freenove Computer Case Kit, running on a Raspberry Pi 5 with Kali Linux.

## Project Overview

This project serves as the **foundational hardware abstraction layer** for the system. It contains stable, reliable, and well-documented code for interacting with the case's integrated hardware, including:

*   OLED Display
*   Addressable RGB LEDs
*   Cooling Fans and Temperature Sensors
*   Camera Module

The code in this repository is considered the **gold standard** for hardware interaction. It is designed to be a dependable backbone that other projects can and should rely on for any hardware-related functionality.

## Gemini's Role

My primary function within this project is to:

1.  **Maintain Stability:** Ensure that any changes or additions to the hardware control code are robust, efficient, and adhere to the project's high standards.
2.  **Identify Synergies:** Proactively identify opportunities to leverage this foundational hardware code in other projects, such as `hacker_basics` or `Noob_Linux_stuff`. When a task in another repository requires hardware interaction (e.g., displaying status on the OLED, using the camera), I will treat this repository as the canonical source for that functionality.
3.  **Enforce Modularity:** Keep the hardware control logic cleanly separated and well-documented, ensuring it remains a reliable and easy-to-use API for other applications.
4.  **Camera Setup (Kali Linux on Raspberry Pi 5):** Undertook extensive troubleshooting and installation of `libcamera` development tools and `rpicam-apps` from source to address camera detection issues on Kali Linux. This involved resolving numerous build dependencies (`meson`, `ninja`, `boost`, `libdrm`, `libavcodec`, `libexif`, `libtiff`, `libpng`, `pkg-config`, etc.). The `rpicam-apps` are now installed, but the system still reports no cameras available, requiring user intervention to verify physical connection and `raspi-config` settings.