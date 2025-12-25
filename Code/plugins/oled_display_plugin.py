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
            if self.oled_screen == 0:
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
            self.oled_screen = (self.oled_screen + 1) % 3
        
        self.oled_counter += 1
