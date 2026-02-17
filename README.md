## Freenove_Computer_Case_Kit_for_Raspberry_Pi

> A computer case kit for Raspberry Pi 5.
* FNK0100A
<img src='Picture/FNK0100A.png' width='100%'/>

* FNK0100B
<img src='Picture/FNK0100B.png' width='100%'/>

* FNK0100H
<img src='Picture/FNK0100H.png' width='100%'/>

* FNK0100K
<img src='Picture/FNK0100K.png' width='100%'/>

### Download

* **Use command in console**

	Run following command to download all the files in this repository.

	git clone https://github.com/Freenove/Freenove_Computer_Case_Kit_for_Raspberry_Pi.git

* **Manually download in browser**

	Click the green "Clone or download" button, then click "Download ZIP" button in the pop-up window.
	Do NOT click the "Open in Desktop" button, it will lead you to install Github software.

> If you meet any difficulties, please contact our support team for help.

### Support

Freenove provides free and quick customer support. Including but not limited to:

* Quality problems of products
* Using Problems of products
* Questions of learning and creation
* Opinions and suggestions
* Ideas and thoughts

Please send an email to:

[support@freenove.com](mailto:support@freenove.com)

We will reply to you within one working day.

### Purchase

Please visit the following page to purchase our products:

http://store.freenove.com

Business customers please contact us through the following email address:

[sale@freenove.com](mailto:sale@freenove.com)

### Copyright

All the files in this repository are released under [Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License](http://creativecommons.org/licenses/by-nc-sa/3.0/).

![markdown](https://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png)

This means you can use them on your own derived works, in part or completely. But NOT for the purpose of commercial use.
You can find a copy of the license in this repository.

Freenove brand and logo are copyright of Freenove Creative Technology Co., Ltd. Can't be used without formal permission.


### About

Freenove is an open-source electronics platform.

Freenove is committed to helping customer quickly realize the creative idea and product prototypes, making it easy to get started for enthusiasts of programing and electronics and launching innovative open source products.

Our services include:

* Robot kits
* Learning kits for Arduino, Raspberry Pi and micro:bit
* Electronic components and modules, tools
* Product customization service

Our code and circuit are open source. You can obtain the details and the latest information through visiting the following web site:

http://www.freenove.com

### Camera Setup and Troubleshooting on Kali Linux (Raspberry Pi 5)

This section details the steps taken to enable and troubleshoot camera functionality on a Raspberry Pi 5 running Kali Linux, and outlines further actions required from the user.

**What has been done (Agent's actions):**

To address initial issues with camera detection and module loading, the following steps were performed:

1.  **Python Environment Setup:**
    *   The project's Python virtual environment (`.venv`) was recreated with the `--system-site-packages` flag to allow access to system-wide installed Python modules (like `libcamera`'s Python bindings).
    *   All necessary Python dependencies for the project, including `picamera2`, were reinstalled within this new virtual environment.

2.  **`picamera2` Dependency Resolution (Bypass `DrmPreview`):**
    *   During attempts to run the `Code/camera.py` example, a `ModuleNotFoundError: No module named 'pykms'` was encountered, stemming from `picamera2`'s `DrmPreview` component.
    *   To bypass this, the `picamera2` library files within the virtual environment were modified to comment out all references to `DrmPreview`. This allowed the Python code to run past this dependency, although it still requires a functioning camera.

3.  **`libcamera` Toolchain Setup:**
    *   The standard `libcamera` command-line tools (`libcamera-still`, `libcamera-hello`, `libcamera-vid`), which are often used for basic camera testing, were initially unavailable in Kali Linux repositories under the expected `libcamera-apps` package.
    *   The `rpicam-apps` (the renamed official Raspberry Pi camera applications) were identified as the source for these tools.
    *   The following build dependencies were installed using `apt`:
        *   `meson`
        *   `ninja-build`
        *   `libyaml-dev`
        *   `libcamera-dev`
        *   `libboost-dev`
        *   `libboost-program-options-dev`
        *   `libavcodec-dev`
        *   `libexif-dev`
        *   `libavdevice-dev`
        *   `libjpeg-dev`
        *   `libtiff-dev`
        *   `libpng-dev`
        *   `pkg-config`
    *   The `rpicam-apps` repository was cloned from `https://github.com/raspberrypi/rpicam-apps.git`.
    *   The applications were successfully built from source using `meson` and `ninja`.
    *   The built applications (`rpicam-still`, `rpicam-hello`, etc.) were installed to `/usr/local/bin`.
    *   The system's dynamic linker cache was updated by running `sudo ldconfig` to ensure the newly installed shared libraries (`librpicam_app.so.1`) could be found.

4.  **Current Status:**
    *   The `rpicam-hello` command-line tool now executes successfully.
    *   However, `rpicam-hello --list-cameras` reports: "No cameras available!". This indicates that while the software is correctly installed, the system's kernel or firmware is not detecting the camera module.

**What you need to do (User's actions):**

To resolve the "No cameras available!" issue and enable camera functionality, please perform the following checks and configurations on your Raspberry Pi 5 running Kali Linux:

1.  **Verify Physical Camera Connection:**
    *   **Action:** Power down your Raspberry Pi completely. Carefully check that the camera module's ribbon cable is securely inserted into the CSI (Camera Serial Interface) port on the Raspberry Pi board. Ensure it is correctly oriented and fully seated.

2.  **Enable Camera Module via `raspi-config`:**
    *   The camera interface needs to be enabled at the firmware level.
    *   **Action:** Open a terminal on your Raspberry Pi and run the command:
        ```bash
        sudo raspi-config
        ```
    *   **Navigation:**
        *   Navigate to `3 Interface Options` (or a similar menu entry).
        *   Select `P1 Camera` (or `Legacy Camera`).
        *   Choose `<Yes>` to enable the camera interface.
        *   If prompted about "Legacy Camera," ensure it's **disabled** (select `No`) as `picamera2` and `libcamera` use the modern camera stack.
        *   Select `<Finish>` and reboot your Raspberry Pi when prompted.

3.  **Test Camera Detection:**
    *   **Action:** After rebooting, open a terminal and run the command:
        ```bash
        rpicam-hello --list-cameras
        ```
    *   **Expected Outcome:** If the camera is now detected, it should list your camera module (e.g., "0: imx708 [4608x2592]").
    *   You can also try a quick preview:
        ```bash
        rpicam-hello
        ```
        (This should open a preview window from your camera for 5 seconds).

Once these steps are completed and the `rpicam-hello --list-cameras` command successfully lists your camera, the Python example `Code/camera.py` should also function correctly. Please inform me of your progress.

---

### Peripherals

| Device | Interface | Capabilities |
|--------|-----------|-------------|
| RTL8812AU USB WiFi Adapter | USB | Dual-band 2.4/5 GHz, monitor mode, packet injection |
| Raspberry Pi Camera Module | CSI | rpicam-apps (built from source for Kali) |

- **WiFi driver:** [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) v5.6.4.2, DKMS install
- **Usage docs:** [Security_Research/10-Hardware-Attacks/WiFi-Adapter/RTL8812AU.md](https://github.com/jayfirns/Security_Research/blob/main/10-Hardware-Attacks/WiFi-Adapter/RTL8812AU.md)

---

### Security Research Integration

This Cyberdeck has been integrated with the [Security Research](../Security_Research) toolkit to provide visual feedback during security operations.

**Features:**
- **LED Status Indicators**: LEDs change color based on current operation
  - Red = WiFi scanning
  - Yellow = Reconnaissance/OpSec check
  - Blue = Network scanning
  - Green = OpSec verified (VPN active)
  - Red flash = Alert/Error
- **OLED Security Screen**: When security tools are running, the OLED shows:
  - Current operation phase
  - Target (IP, interface)
  - Progress bar
  - Status messages

**Documentation:**
- [Security Integration Plugin](Code/plugins/SECURITY_INTEGRATION.md) - Cyberdeck-side integration
- [Hardware Bridge API](../Security_Research/13-Utils/HARDWARE_BRIDGE.md) - Security tools API

**Quick Test:**
```bash
# Terminal 1: Start Cyberdeck
cd Code && python application.py

# Terminal 2: Run demo
cd ../Security_Research/13-Utils
python test_hardware_bridge.py --demo
```

---

## Related Repositories

- [Security_Research](https://github.com/jayfirns/Security_Research) — Structured security workflows and automation
- [rtl8812au](https://github.com/jayfirns/rtl8812au) — WiFi adapter driver fork (RTL8812AU)
