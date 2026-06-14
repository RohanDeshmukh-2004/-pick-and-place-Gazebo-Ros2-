from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'pick_and_place'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Launch files
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
        # World files
        (os.path.join('share', package_name, 'worlds'),
            glob('worlds/*.sdf')),
        # Config files
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Rohan Deshmukh',
    maintainer_email='rohanofficials123@gmail.com',
    description='Autonomous vision-guided pick and place using ROS 2, MoveIt2, OpenCV and Gazebo',
    license='MIT',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'object_detector = pick_and_place.object_detector:main',
            'pick_and_place_node = pick_and_place.pick_and_place_node:main',
        ],
    },
)
