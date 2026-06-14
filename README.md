# 🤖 Autonomous Pick and Place — ROS 2 + MoveIt2 + OpenCV

> Vision-guided autonomous pick-and-place on a UR5 robotic arm using ROS 2 Humble, MoveIt2, and OpenCV-based object detection in Gazebo simulation.

---

## 📽️ Demo

![Pick and Place Demo](demo.gif)

---

## 🧠 What It Does

- Spawns a **UR5 robotic arm** in a Gazebo simulation environment with a table and colored objects
- A **simulated RGB camera** mounted above the table captures the scene
- An **OpenCV node** detects colored objects (red, green, blue) and computes their 3D positions
- A **MoveIt2 pick-and-place node** plans and executes the full pick and place sequence

---

## 🏗️ System Architecture

cat > ~/ros2_ws/src/pick_and_place/README.md << 'EOF'
# 🤖 Autonomous Pick and Place — ROS 2 + MoveIt2 + OpenCV

> Vision-guided autonomous pick-and-place on a UR5 robotic arm using ROS 2 Humble, MoveIt2, and OpenCV-based object detection in Gazebo simulation.

---

## 📽️ Demo

![Pick and Place Demo](demo.gif)

---

## 🧠 What It Does

- Spawns a **UR5 robotic arm** in a Gazebo simulation environment with a table and colored objects
- A **simulated RGB camera** mounted above the table captures the scene
- An **OpenCV node** detects colored objects (red, green, blue) and computes their 3D positions
- A **MoveIt2 pick-and-place node** plans and executes the full pick and place sequence

---

## 🏗️ System Architecture



Gazebo Simulation

│

▼

/camera/image_raw

│

▼

object_detector.py  ──►  OpenCV HSV color filtering

│

▼

/detected_objects  (x,y,z positions)

│

▼

pick_and_place_node.py  ──►  MoveIt2 motion planning

│

▼

UR5 arm picks and places objects

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Robot | UR5 (Universal Robots) |
| Simulation | Gazebo Classic |
| Motion Planning | MoveIt2 |
| Object Detection | OpenCV (HSV color filtering) |
| Framework | ROS 2 Humble |
| Language | Python 3 |

---

## 📁 Project Structure
pick_and_place/

├── pick_and_place/

│   ├── object_detector.py       # OpenCV color detection node

│   └── pick_and_place_node.py   # MoveIt2 pick and place logic

├── launch/

│   ├── sim.launch.py            # Launches Gazebo + UR5

│   └── pick_and_place.launch.py # Launches full pipeline

├── worlds/

│   └── pick_world.sdf           # Custom Gazebo world

├── config/

│   └── colors.yaml              # HSV color ranges

├── setup.py

└── package.xml
---

## ⚙️ Setup & Installation

### Prerequisites
- Ubuntu 22.04
- ROS 2 Humble
- MoveIt2
- Gazebo Classic 11

### Install Dependencies

```bash
sudo apt install ros-humble-ur-description ros-humble-ur-moveit-config ros-humble-ur-ros2-driver
cd ~/ros2_ws/src
git clone -b humble https://github.com/UniversalRobots/Universal_Robots_ROS2_Gazebo_Simulation.git
```

### Clone and Build

```bash
cd ~/ros2_ws/src
git clone https://github.com/RohanDeshmukh-2004/pick-and-place-ros2.git pick_and_place
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select pick_and_place
source install/setup.bash
```

---

## 🚀 How to Run

```bash
ros2 launch pick_and_place pick_and_place.launch.py
```

---

## 👤 Author

**Rohan Deshmukh**
B.Tech ECE, IIITDM Kancheepuram (2023–2027)
Robotics Intern, IIT Dharwad

- 🔗 [LinkedIn](https://linkedin.com/in/rohan-deshmukh-168926307)
- 💻 [GitHub](https://github.com/RohanDeshmukh-2004)

---

## 📄 License

MIT License
