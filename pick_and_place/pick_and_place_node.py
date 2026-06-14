import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Pose
from std_msgs.msg import String
import time

from moveit.planning import MoveItPy
from moveit.core.robot_state import RobotState


class PickAndPlaceNode(Node):

    def __init__(self):
        super().__init__('pick_and_place_node')

        # MoveIt2 init
        self.moveit = MoveItPy(node_name='pick_and_place_moveit')
        self.arm = self.moveit.get_planning_component('ur_arm')
        self.get_logger().info('MoveIt2 Ready')

        # Place zone from config
        self.place_x = 0.3
        self.place_y = -0.3
        self.place_z = 0.25

        # State tracking
        self.current_color = None
        self.picking = False

        # Subscribe to detected object position and color
        self.pos_sub = self.create_subscription(
            Point,
            '/detected_objects',
            self.position_callback,
            10
        )
        self.color_sub = self.create_subscription(
            String,
            '/detected_color',
            self.color_callback,
            10
        )

        self.get_logger().info('Pick and Place Node Started')

    def color_callback(self, msg):
        self.current_color = msg.data

    def position_callback(self, msg):
        # Skip if already picking
        if self.picking:
            return

        self.picking = True
        self.get_logger().info(
            f'Picking {self.current_color} ball at '
            f'x={msg.x:.2f}, y={msg.y:.2f}, z={msg.z:.2f}'
        )

        # Execute pick and place sequence
        self.execute_pick(msg.x, msg.y, msg.z)
        self.execute_place()

        self.picking = False

    def move_to_pose(self, x, y, z):
        # Set target pose
        pose = Pose()
        pose.position.x = x
        pose.position.y = y
        pose.position.z = z

        # Orientation — pointing down
        pose.orientation.x = 0.0
        pose.orientation.y = 1.0
        pose.orientation.z = 0.0
        pose.orientation.w = 0.0

        self.arm.set_goal_state(pose_stamped_msg=pose, pose_link='tool0')

        # Plan and execute
        plan = self.arm.plan()
        if plan:
            self.moveit.execute(plan, controllers=[])
            self.get_logger().info(f'Moved to x={x:.2f}, y={y:.2f}, z={z:.2f}')
        else:
            self.get_logger().error('Planning failed!')

    def execute_pick(self, x, y, z):
        # Step 1 — move above object
        self.get_logger().info('Moving above object...')
        self.move_to_pose(x, y, z + 0.15)
        time.sleep(1.0)

        # Step 2 — move down to grasp
        self.get_logger().info('Moving down to grasp...')
        self.move_to_pose(x, y, z)
        time.sleep(0.5)

        # Step 3 — close gripper
        self.get_logger().info('Closing gripper...')
        self.close_gripper()
        time.sleep(0.5)

        # Step 4 — lift up
        self.get_logger().info('Lifting object...')
        self.move_to_pose(x, y, z + 0.2)
        time.sleep(1.0)

    def execute_place(self):
        # Step 5 — move to place zone
        self.get_logger().info('Moving to place zone...')
        self.move_to_pose(self.place_x, self.place_y, self.place_z + 0.1)
        time.sleep(1.0)

        # Step 6 — move down
        self.move_to_pose(self.place_x, self.place_y, self.place_z)
        time.sleep(0.5)

        # Step 7 — open gripper
        self.get_logger().info('Opening gripper...')
        self.open_gripper()
        time.sleep(0.5)

        # Step 8 — move back up
        self.move_to_pose(self.place_x, self.place_y, self.place_z + 0.2)

    def close_gripper(self):
        gripper = self.moveit.get_planning_component('gripper')
        gripper.set_goal_state(configuration_name='closed')
        plan = gripper.plan()
        if plan:
            self.moveit.execute(plan, controllers=[])

    def open_gripper(self):
        gripper = self.moveit.get_planning_component('gripper')
        gripper.set_goal_state(configuration_name='open')
        plan = gripper.plan()
        if plan:
            self.moveit.execute(plan, controllers=[])


def main(args=None):
    rclpy.init(args=args)
    node = PickAndPlaceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
