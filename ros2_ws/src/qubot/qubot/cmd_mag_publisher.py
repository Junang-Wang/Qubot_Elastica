#! /home/qubot/.pyenv/shims/python3
import rclpy 
from rclpy.node import Node 
from action_interfaces.msg import MagneticSpherical
from .utils import PCB
import threading

class ListenPCBNode(Node):

    def __init__(self):
        super().__init__('ListenPCB')
        self.cmd_mag_pub = self.create_publisher(MagneticSpherical, "/controller/cmd_mag", 10)
        self.serial = PCB()
        # self.timer = self.create_timer(0.5,self.send_velocity_command)
        self.send_mag_command()
        self.get_logger().info('Listening PCB magnetic field spherical')
    
    def send_mag_command(self):
        msg = MagneticSpherical()
        msg.magnetic_field_spherical = self.serial.magnetic_field_spherical
        # msg.magnetic_field_spherical = [0.0,0.0,0.0]
        
        task_PCB_read = threading.Thread(target=self.serial.PCB_read, args=(self.cmd_mag_pub,msg), name='t1')
        task_PCB_read.start()
        # self.serial.PCB_read()
        self.get_logger().info('publishing mag msg')
        

                

def main(args=None):
    rclpy.init(args=args)
    node = ListenPCBNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()