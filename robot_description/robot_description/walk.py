import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from robot_description.invKin import leg_chain
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import numpy as np
from builtin_interfaces.msg import Duration
class WalkNode(Node): 
    def __init__(self):
         super().__init__('walk_node')

         self.subscription = self.create_subscription(
            Float32,
            'angle_topic',
            self.listener_callback,
            10)
         
         self.publisher = self.create_publisher(JointTrajectory,
                                                '/leg1_controller/joint_trajectory', 
                                                 10 )
        
         self.joint_names = ['hip_joint', 'shoulder_joint','knee_joint' ]
    
         self.current_angle = None

         timer_period = 2.0
        
         self.timer = self.create_timer(timer_period, self.timer_callback)
        
    def listener_callback(self, msg):
            self.current_angle = msg.data


    def timer_callback(self): 
        if self.current_angle is not None:
            
            theta = self.current_angle
            self.get_logger().info(f'Angle: {self.current_angle}')

            walk_points = []
            
            straightLineY = [-5, -2.5, 0, 2.5, 5]

            for y in [5, 2.5, 0, -2.5, -5]:
                walk_points.append([2.5 -y*np.sin(theta), y*np.cos(theta), -25])

            for y in straightLineY:
                z = 7.5*np.cos((np.pi/12)*y) - 25
                walk_points.append([2.5 -y*np.sin(theta), y*np.cos(theta), z])

            counter = 0
            points = []

            for point in walk_points: 
                counter += 1
                angles = leg_chain.inverse_kinematics(target_position=point)
                angles = angles[1:4].tolist()
                
                pt = JointTrajectoryPoint()
                pt.positions = angles
                
                t = 0.2*counter    
                pt.time_from_start = Duration(
                    sec=int(t),
                    nanosec=int((t - int(t)) * 1e9)
                )
                    
                points.append(pt)

            msg = JointTrajectory()
            msg.joint_names = self.joint_names
            msg.points = points

            self.publisher.publish(msg)
                   





def main(args=None):
    rclpy.init(args=args)

    walk_node = WalkNode()

    rclpy.spin(walk_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    walk_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
