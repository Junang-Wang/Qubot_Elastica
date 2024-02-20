#! /home/qubot/.pyenv/shims/python3
import rclpy
from rclpy.node import Node
from action_interfaces.msg import MagneticSpherical 
class PoseSubscriberNode(Node):

    def __init__(self):
        super().__init__('pose_subscriber')
        self.pose_subscriber_ = self.create_subscription(MagneticSpherical,"/controller/cmd_mag", self.pose_callback, 10)

    def pose_callback(self,msg:MagneticSpherical):
        self.get_logger().info(msg)



def main(args=None):
    rclpy.init(args=args)
    node = PoseSubscriberNode()
    rclpy.spin(node)
    rclpy.shutdown()