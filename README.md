# Serving_Robot_Simulation

## 개발 환경
Ubuntu 20.04 Foxy

## 주의 사항
map.yaml & map.pgm 파일은 home 디렉토리에 위치

만약 gazebo error시 다음 코드 터미널에 입력
~~~
$ source /usr/share/gazebo/setup.sh
~~~

## 설치 방법 & 환경 설정
~~~
$ git clone https://github.com/Robot-Programming-Serving-Robot/Serving_Robot_Simulation.git
$ cd Serving_Robot_Simulation
$ colcon build
$ source ~/Serving_Robot_Simulation/install/setup.bash
$ echo "source ~/Serving_Robot_Simulation/install/setup.bash" >> ~/.bashrc
$ echo "export TURTLEBOT3_MODEL=waffle" >> ~/.bashrc
$ echo "export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/opt/ros/foxy/share/turtlebot3_gazebo/models" >> ~/.bashrc
~~~

## 실행 방법
총 4개의 터미널 활용
~~~
$ ros2 launch turtlebot3_gazebo turtlebot3_cafe.launch.py
$ ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/map.yaml
$ ros2 run order_action order_action_server
$ ros2 action send_goal /order action_interfaces/action/Order “{orders: [num1, num2, num3, num4 ...]}”
### num1, num2, num3, num4 부분에 1~4의 숫자 대입, 짝수개만 입력

### 실행 예시
$ ros2 action send_goal /order action_interfaces/action/Order “{orders: [1, 2, 1, 3]}”
~~~
