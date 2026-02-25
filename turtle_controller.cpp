#include <memory>
#include <chrono>
#include <cmath>
#include <string>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "turtlesim/msg/pose.hpp"
#include "example_interfaces/srv/set_bool.hpp" // Ejemplo para simplificar set_mode
#include "rclcpp_action/rclcpp_action.hpp"

// Sustituir por una interfaz de acción personalizada si es necesario
// Aquí se ilustra la lógica descrita en el diseño [cite: 48-56]

using namespace std::chrono_literals;

class TurtleController : public rclcpp::Node {
public:
    TurtleController() : Node("turtle_controller_node"), mode_(0) {
        // 1. Publicador de velocidades [cite: 30]
        velocity_publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);

        // 2. Suscriptor de pose para navegación [cite: 30]
        pose_subscriber_ = this->create_subscription<turtlesim::msg::Pose>(
            "/turtle1/pose", 10, std::bind(&TurtleController::pose_callback, this, std::placeholders::_1));

        // 3. Servidor de Servicio para cambiar modo [cite: 31, 36]
        // En el informe se menciona un servicio para cambios instantáneos
        mode_service_ = this->create_service<example_interfaces::srv::SetBool>(
            "set_mode", std::bind(&TurtleController::handle_set_mode, this, std::placeholders::_1, std::placeholders::_2));

        // Timer para el bucle de control (Modo Circular) [cite: 41]
        timer_ = this->create_wall_timer(100ms, std::bind(&TurtleController::control_loop, this));
        
        RCLCPP_INFO(this->get_logger(), "Nodo controlador iniciado (MODO MANUAL)");
    }

private:
    // Lógica de cambio de modo vía Servicio [cite: 36]
    void handle_set_mode(const std::shared_ptr<example_interfaces::srv::SetBool::Request> request,
                         std::shared_ptr<example_interfaces::srv::SetBool::Response> response) {
        if (request->data) {
            mode_ = 1; // Modo Circular
            RCLCPP_INFO(this->get_logger(), "Cambiando a Modo Autónomo Circular");
        } else {
            mode_ = 0; // Modo Manual
            RCLCPP_INFO(this->get_logger(), "Cambiando a Modo Manual");
        }
        response->success = true;
    }

    void pose_callback(const turtlesim::msg::Pose::SharedPtr msg) {
        current_pose_ = *msg;
    }

    void control_loop() {
        auto drive_msg = geometry_msgs::msg::Twist();

        if (mode_ == 1) { // MODO CIRCULAR [cite: 40]
            // v = constante, w = constante [cite: 42, 43]
            drive_msg.linear.x = 2.0;
            drive_msg.angular.z = 1.0; // >0 para antihorario [cite: 45, 46]
            velocity_publisher_->publish(drive_msg);
        }
        // En Modo Manual (0), el nodo no genera comandos, permitiendo teleop externo [cite: 38, 39]
    }

    // Variables de estado
    int mode_; 
    turtlesim::msg::Pose current_pose_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr velocity_publisher_;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pose_subscriber_;
    rclcpp::Service<example_interfaces::srv::SetBool>::SharedPtr mode_service_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TurtleController>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
