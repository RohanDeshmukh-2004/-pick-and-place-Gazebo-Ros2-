import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import numpy as np
import yaml
import os
from ament_index_python.packages import get_package_share_directory


class ObjectDetector(Node):

    def __init__(self):
        super().__init__('object_detector')

        # CV Bridge — converts ROS image to OpenCV image
        self.bridge = CvBridge()

        # Load color config
        config_path = os.path.join(
            get_package_share_directory('pick_and_place'),
            'config', 'colors.yaml'
        )
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Camera height above table (meters) — for pixel to world conversion
        self.camera_height = 1.5
        self.table_height = 0.05

        # Subscribe to camera topic
        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # Publish detected object positions
        self.object_pub = self.create_publisher(Point, '/detected_objects', 10)
        self.color_pub = self.create_publisher(String, '/detected_color', 10)

        self.get_logger().info('Object Detector Node Started')

    def image_callback(self, msg):
        # Convert ROS image to OpenCV
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        colors = self.config['colors']

        for color_name, ranges in colors.items():
            lower = np.array(ranges['lower'], dtype=np.uint8)
            upper = np.array(ranges['upper'], dtype=np.uint8)
            mask = cv2.inRange(hsv, lower, upper)

            # Red has two ranges in HSV
            if 'lower2' in ranges:
                lower2 = np.array(ranges['lower2'], dtype=np.uint8)
                upper2 = np.array(ranges['upper2'], dtype=np.uint8)
                mask2 = cv2.inRange(hsv, lower2, upper2)
                mask = cv2.bitwise_or(mask, mask2)

            # Find contours
            contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            for contour in contours:
                area = cv2.contourArea(contour)

                # Filter small noise
                if area < 500:
                    continue

                # Get center of detected object
                M = cv2.moments(contour)
                if M['m00'] == 0:
                    continue

                # Pixel coordinates of center
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])

                # Convert pixel to world coordinates
                world_x, world_y = self.pixel_to_world(
                    cx, cy,
                    frame.shape[1],
                    frame.shape[0]
                )

                # Publish position
                point = Point()
                point.x = world_x
                point.y = world_y
                point.z = self.table_height + 0.025  # table height + ball radius

                self.object_pub.publish(point)

                # Publish color
                color_msg = String()
                color_msg.data = color_name
                self.color_pub.publish(color_msg)

                self.get_logger().info(
                    f'Detected {color_name} ball at '
                    f'x={world_x:.2f}, y={world_y:.2f}'
                )

    def pixel_to_world(self, px, py, img_width, img_height):
        # Camera FOV = 60 degrees (1.047 rad)
        # Camera at height 1.5m looking straight down
        fov = 1.047
        effective_height = self.camera_height - self.table_height

        # Width and height of view at table level
        view_width = 2 * effective_height * np.tan(fov / 2)
        view_height = view_width * (img_height / img_width)

        # Normalize pixel to [-0.5, 0.5]
        norm_x = (px / img_width) - 0.5
        norm_y = (py / img_height) - 0.5

        # World coordinates (camera centered at x=0.5, y=0)
        world_x = 0.5 + norm_x * view_width
        world_y = -norm_y * view_height  # flip y axis

        return world_x, world_y


def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
