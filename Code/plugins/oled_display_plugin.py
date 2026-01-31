from plugins.base_plugin import BasePlugin

class OledDisplayPlugin(BasePlugin):
    def __init__(self, oled):
        super().__init__()
        self.oled = oled
        self.font_size = 12
        self.oled_counter = 0
        self.oled_screen = 0

    def update(self, pi_monitor):
        if self.oled_counter % 3 == 0:
            self.oled.clear()

            # Check if security mode is active - if so, show security screen
            security_plugin = pi_monitor.plugins.get('security_status')
            security_active = (
                security_plugin and
                security_plugin.current_mode != 'idle'
            )

            if security_active:
                # Security screen takes over when active
                self._draw_security_screen(pi_monitor, security_plugin)
            elif self.oled_screen == 0:
                # Screen 1: System Parameters
                self.oled.draw_text("PI Parameters", position=(0, 0), font_size=self.font_size)
                self.oled.draw_text(pi_monitor._format_strings['cpu'].format(pi_monitor.plugins['cpu_monitor'].cpu_usage), position=(0, 16), font_size=self.font_size)
                self.oled.draw_text(pi_monitor._format_strings['mem'].format(pi_monitor.plugins['memory_monitor'].memory_usage), position=(0, 32), font_size=self.font_size)
                self.oled.draw_text(pi_monitor._format_strings['disk'].format(pi_monitor.plugins['disk_monitor'].disk_usage), position=(0, 48), font_size=self.font_size)
            elif self.oled_screen == 1:
                # Screen 2: Date/Time/LED
                self.oled.draw_text(pi_monitor._format_strings['date'].format(pi_monitor.get_raspberry_date()), position=(0, 0), font_size=self.font_size)
                self.oled.draw_text(pi_monitor._format_strings['week'].format(pi_monitor.get_raspberry_weekday()), position=(0, 16), font_size=self.font_size)
                self.oled.draw_text(pi_monitor._format_strings['time'].format(pi_monitor.get_raspberry_time()), position=(0, 32), font_size=self.font_size)
                self.oled.draw_text(pi_monitor._format_strings['led_mode'].format(pi_monitor.get_computer_led_mode()), position=(0, 48), font_size=self.font_size)
            else:  # oled_screen == 2
                # Screen 3: Temperature/Fan
                self.oled.draw_text(pi_monitor._format_strings['pi_temp'].format(pi_monitor.plugins['cpu_temp'].cpu_temperature), position=(0, 0), font_size=self.font_size)
                self.oled.draw_text(pi_monitor._format_strings['pc_temp'].format(pi_monitor.get_computer_temperature()), position=(0, 16), font_size=self.font_size)
                self.oled.draw_text(pi_monitor._format_strings['fan_mode'].format(pi_monitor.get_computer_fan_mode()), position=(0, 32), font_size=self.font_size)
                self.oled.draw_text(pi_monitor._format_strings['fan_duty'].format(int(float(pi_monitor.get_computer_fan_duty()/255.0)*100)), position=(0, 48), font_size=self.font_size)

            self.oled.show()

            # Only rotate screens when not in security mode
            if not security_active:
                self.oled_screen = (self.oled_screen + 1) % 3

        self.oled_counter += 1

    def _draw_security_screen(self, pi_monitor, security_plugin):
        """Draw security operation status screen."""
        mode = security_plugin.current_mode.upper()
        phase = security_plugin.current_phase or mode
        target = security_plugin.current_target or ''
        message = security_plugin.current_message or ''
        progress = security_plugin.current_progress

        # Line 1: Mode/Phase header
        header = f"[{phase[:18]}]"
        self.oled.draw_text(header, position=(0, 0), font_size=self.font_size)

        # Line 2: Target
        if target:
            target_line = f"TGT: {target[:16]}"
            self.oled.draw_text(target_line, position=(0, 16), font_size=self.font_size)

        # Line 3: Progress bar (if available)
        if progress is not None:
            bar = security_plugin.get_progress_bar(14)
            pct = int((progress / (security_plugin.progress_max or 100)) * 100)
            progress_line = f"{bar} {pct}%"
            self.oled.draw_text(progress_line, position=(0, 32), font_size=self.font_size)
        elif message:
            # Show message on line 3 if no progress
            self.oled.draw_text(message[:20], position=(0, 32), font_size=self.font_size)

        # Line 4: Message or details
        if progress is not None and message:
            self.oled.draw_text(message[:20], position=(0, 48), font_size=self.font_size)
        else:
            # Show channel info for wifi scanning
            details = security_plugin.details
            if 'channel' in details:
                self.oled.draw_text(f"CH: {details['channel']}", position=(0, 48), font_size=self.font_size)
