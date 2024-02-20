#! /home/qubot/.pyenv/shims/python3
import rclpy
from rclpy.node import Node
from action_interfaces.msg import MagneticSpherical 
class MagSubscriberNode(Node):

    def __init__(self):
        super().__init__('mag_subscriber')
        self.get_logger().info('Hello')
        self.mag_subscriber_ = self.create_subscription(MagneticSpherical,"/controller/cmd_mag", self.mag_callback, 10)

    def mag_callback(self,msg:MagneticSpherical):
        self.get_logger().info('subscribe mag msg')
        self.get_logger().info(str(msg.magnetic_field_spherical))



def main(args=None):
    rclpy.init(args=args)
    node = MagSubscriberNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ =='__main__':
    main()