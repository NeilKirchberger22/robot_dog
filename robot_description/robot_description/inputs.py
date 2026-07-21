import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class InputReceiver(Node): 
    def __init__(self):
        super().__init__('input_node')

        self.publisher = self.create_publisher(
            Float32,
            'angle_topic', 
            10)
        
        self.current_angle = None 

    def receive(self): 
        msg = Float32()
        
        while rclpy.ok(): 
            self.current_angle = float(input("Enter an angle: "))
            msg.data = self.current_angle
            self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    input_node = InputReceiver()

    input_node.receive()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    input_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

