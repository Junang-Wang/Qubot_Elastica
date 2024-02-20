#!/usr/bin/env python3
import rclpy
from rclpy.lifecycle import LifecycleNode
from example_interfaces.msg import Int64
from rclpy.lifecycle.node import LifecycleState, TransitionCallbackReturn

class NumberPublisherNode(LifecycleNode):
    def __init__(self):
        super().__init__("number_publisher")
        self.get_logger().info('IN constructor')
        self.number_ = 1
        self.publish_frequency_ = 1.0
        self.number_publisher_ = None 
        self.number_timer_ = None

    # Create ROS2 communication, connect to Hardware
    def on_configure(self, previous_state: LifecycleState):

        self.get_logger().info("IN on_configure")
        self.number_publisher_ = self.create_publisher(Int64, "number", 10)
        self.number_timer_ = self.create_timer(
            1.0 / self.publish_frequency_, self.publish_number)
        
        return TransitionCallbackReturn.Success
    
    # Destroy ROS2 communications, disconnect from Hardware
    def on_cleanup(self, previous_state:LifecycleState):
        self.get_logger().info('IN on_cleanup')
        self.destroy_lifecycle_publisher(self.number_publisher_)
        self.destroy_timer(self.number_timer_)
        return TransitionCallbackReturn.SUCCESS
    
    # Activate/Enable Hardware
    def on_activate(self, previous_state: LifecycleState):
        self.get_logger().info("IN on active")
        return super().on_activate(previous_state)
    
    # Deactivate/Disable Hardware
    def on_deactivate(self, previous_state: LifecycleState):
        self.get_logger().info("IN on deactivate")
        return super().on_deactivate(previous_state)
    
    def on_shutdown(self, previous_state: LifecycleState):
        self.destroy_lifecycle_publisher(self.number_publisher_)
        self.destroy_timer(self.number_timer_)
        return TransitionCallbackReturn.SUCCESS
        

    

    def publish_number(self):
        msg = Int64()
        msg.data = self.number_
        self.number_publisher_.publish(msg)
        self.number_ += 1

def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()
