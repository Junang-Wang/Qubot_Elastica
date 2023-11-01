
def draw_text(screen, text, color, x, y, font):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))


class PIDController:
    def __init__(self, Kp, Ki, Kd, target_angle):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.target_angle = target_angle
        self.previous_error = 0
        self.integral = 0
        self.magnetic_amplitude_max = 50

    def calculate_control_signal(self, current_angle):
        error = self.target_angle - current_angle
        self.integral += error
        derivative = error - self.previous_error
        control_signal = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.previous_error = error
        return control_signal

    @staticmethod
    def calculate_magnetic_amplitude(target_angle, current_angle, magnetic_amplitude):
        pid_controller = PIDController(Kp=0.1, Ki=0.01, Kd=0.01, target_angle=target_angle)
        control_signal = pid_controller.calculate_control_signal(current_angle)
        magnetic_amplitude += control_signal
        
        # 将磁场强度限制在合理的范围内
        if magnetic_amplitude < 0:
            magnetic_amplitude = 0
        elif magnetic_amplitude > PIDController.magnetic_amplitude_max:
            magnetic_amplitude = PIDController.magnetic_amplitude_max
        
        return magnetic_amplitude
