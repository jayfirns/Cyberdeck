from plugins.base_plugin import BasePlugin

class FanControlPlugin(BasePlugin):
    def __init__(self, expansion):
        super().__init__()
        self.expansion = expansion
        self.last_fan_pwm = 0
        self.last_fan_pwm_limit = 0
        self.temp_threshold_high = 170
        self.temp_threshold_low = 130
        self.max_pwm = 255
        self.min_pwm = 0

    def update(self, pi_monitor):
        current_cpu_temp = pi_monitor.plugins['cpu_temp'].cpu_temperature
        current_fan_pwm = pi_monitor.plugins['fan_pwm'].fan_pwm
        
        if current_fan_pwm != -1:
            if self.last_fan_pwm_limit == 0 and current_cpu_temp > self.temp_threshold_high:
                self.last_fan_pwm = self.max_pwm
                self.expansion.set_fan_duty(self.last_fan_pwm, self.last_fan_pwm)
                self.last_fan_pwm_limit = 1
            elif self.last_fan_pwm_limit == 1 and current_cpu_temp < self.temp_threshold_low:
                self.last_fan_pwm = self.min_pwm
                self.expansion.set_fan_duty(self.last_fan_pwm, self.last_fan_pwm)
                self.last_fan_pwm_limit = 0
