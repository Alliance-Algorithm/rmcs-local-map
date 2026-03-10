## RMCS Local Map For Sentry

### 简介

本仓库是从 `rmcs_slam` 的 obstacle 模块独立出来的局部障碍地图包，专门给导航系统提供近场避障输入。

和 `rmcs_slam` 时代相比，这个包做了两件事：

- 只保留单雷达输入链路（1 路 Livox 点云 + 1 路 IMU）
- 参数和发布逻辑按 Nav2 的使用习惯整理，专注发布局部 `OccupancyGrid`

如果你要全局地图、重定位、路径规划，那是其他包的职责，这里不做。

### 部署

#### 环境需求

- 任意 `linux` 发行版
- `ros:humble` 或 `ros:jazzy`（推荐 docker）
- livox mid-360 雷达（或使用 ros2 bag 回放 Livox 消息）

#### 项目依赖

- 激光雷达驱动 `livox-sdk`（系统级安装）

    ```sh
    git clone https://github.com/Livox-SDK/Livox-SDK2.git
    cd Livox-SDK2
    mkdir build && cd build
    cmake .. && make -j
    sudo make install
    ```

- 激光雷达 ROS2 接口 `livox_ros_driver2`（放进同一工作空间）

    ```sh
    cd /path/to/your/ws/src
    git clone https://github.com/Alliance-Algorithm/livox_ros_driver2.git
    cd ..
    colcon build --packages-select livox_ros_driver2
    ```

- 点云处理依赖 `pcl` 及其 ROS2 绑定

    ```sh
    sudo apt-get install -y     \
    ros-$ROS_DISTRO-pcl-conversions \
    ros-$ROS_DISTRO-pcl-ros         \
    libpcl-ros-dev                  \
    libpcl-dev
    ```

- 线性代数库 `eigen`

    ```sh
    sudo apt-get install libeigen3-dev
    ```

如果你想偷懒一把，也可以：

```sh
cd /path/to/your/ws
rosdep install --from-paths src --ignore-src -r -y
```

### 配置项目

本包配置文件在 `config/local_map.yaml`，核心关注下面这几项。

#### 1) Topic 名字

```yaml
lidar:
  lid_topic: "/livox/lidar"
  imu_topic: "/livox/imu"
```

如果你接的是实机 multi_topic 驱动，按你自己的 topic 改；
如果你用你给我的 bag，默认这两个名字就是对的。

#### 2) 雷达安装位姿（底盘系）

```yaml
lidar:
  # x y z
  lidar_translation: [ +0.0, +0.0, +0.60 ]
  # yaw pitch roll (degree)
  lidar_orientation: [ -90.0, 0.0, 180.0 ]
```

这块会直接影响障碍图形状和位置，填错了就会看起来像地图在飘。

#### 3) 地图发布坐标系

```yaml
name:
  grid: "/rmcs_map/map/grid"
  frame: "base_link"
```

这个 `frame` 是给 Nav2 local_costmap 用的，推荐直接用 `base_link`。

#### 4) 地图尺寸与分辨率

```yaml
grid:
  resolution: 0.02
  map_width: 10.1
  map_height: 2.0
```

`map_width` 是正方形边长，单位米；分辨率越细越吃性能。

### 项目构建

```sh
cd /path/to/your/ws
colcon build --packages-select rmcs_local_map
```

如果没看到爆红报错，基本就是成了。

### 使用方法

```sh
source /opt/ros/$ROS_DISTRO/setup.bash
source /path/to/your/ws/install/setup.bash

ros2 launch rmcs_local_map launch.py
```

### 用 ros2 bag 进行测试

你可以直接用 Livox 格式 bag 做联调：

```sh
# 终端 1
ros2 launch rmcs_local_map launch.py

# 终端 2
ros2 bag play /workspaces/data/bag/battlefield_0
```

### 主要输出话题

```text
- /rmcs_map/map/grid           # 局部障碍栅格地图（给导航用）
- /rmcs_map/segmentation_part  # 分割/裁剪后的点云（调试用）
- /livox/lidar/undistort       # 去畸变点云（调试用）
```

### 关于 Nav2 对接

这个包只负责局部障碍地图，建议接到 `local_costmap`，不要拿它替代全局地图。

全局图、定位、规划参数请放在你自己的导航包里维护，这样职责干净，也好查问题。
