# Robot Diferencial – Mini Proyecto ROS 2 Jazzy

## Contenido
Este repositorio contiene el desarrollo completo de un robot diferencial
implementado en ROS 2 Jazzy, incluyendo:

- URDF/Xacro con geometría, colisiones e inercias
- Sensores: cámara, IMU y LiDAR
- Visualización en RViz
- Árbol TF consistente
- Simulación en Gazebo Harmonic

## Ejecución RViz
```bash
ros2 launch dif_bot_description display_tf.launch.py
ros2 run joint_state_publisher joint_state_publisher
rviz2
