import numpy as np
def draw_text(screen, text, color, x, y, font):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))


class PIDController:
    def __init__(self, Kp, Ki, Kd, target_pos, magnetic_amplitude_max, time_step):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.target_pos = target_pos
        self.previous_error = 0
        self.integral = 0
        self.magnetic_amplitude_max = magnetic_amplitude_max
        self.time_step = time_step

    def calculate_control_signal(self, current_pos):
        error = self.target_pos - current_pos
        self.integral += error*self.time_step
        derivative = (error - self.previous_error )/self.time_step
        control_signal = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.previous_error = error
        return control_signal

    @staticmethod
    def calculate_magnetic_field(Kp, Ki, Kd, target_pos, current_pos, magnetic_field, scale_E, magnetic_amplitude_max, time_step):
        pid_controller = PIDController(Kp=Kp, Ki=Ki, Kd=Kd, target_pos=target_pos, magnetic_amplitude_max=magnetic_amplitude_max,time_step=time_step)
        control_signal = pid_controller.calculate_control_signal(current_pos)
        magnetic_field += control_signal
        magnetic_amplitude = np.linalg.norm(magnetic_field)
        magnetic_field_direction = magnetic_field/magnetic_amplitude 
        # 将磁场强度限制在合理的范围内
        if magnetic_amplitude < 0:
            magnetic_amplitude = 0
            magnetic_field -= magnetic_field
        elif magnetic_amplitude > pid_controller.magnetic_amplitude_max * scale_E:
            magnetic_amplitude = pid_controller.magnetic_amplitude_max * scale_E
            magnetic_field += -magnetic_field + magnetic_amplitude*magnetic_field_direction
        
        return magnetic_amplitude/scale_E, magnetic_field/magnetic_amplitude
