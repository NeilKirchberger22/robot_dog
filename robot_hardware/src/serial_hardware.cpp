#include "robot_hardware/serial_hardware.hpp"

#include <cerrno>
#include <cmath>
#include <cstring>
#include <iomanip>
#include <limits>
#include <sstream>
#include <string>

#include <fcntl.h>
#include <termios.h>
#include <unistd.h>

#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include "pluginlib/class_list_macros.hpp"
#include "rclcpp/rclcpp.hpp"

namespace robot_hardware
{

hardware_interface::CallbackReturn RobotHardware::on_init(
  const hardware_interface::HardwareInfo & info)
{
  if (
    hardware_interface::SystemInterface::on_init(info) !=
    hardware_interface::CallbackReturn::SUCCESS)
  {
    return hardware_interface::CallbackReturn::ERROR;
  }

  port_name_ = info_.hardware_parameters["serial_port"];

  positions_.resize(info_.joints.size(), 0.0);
  commands_.resize(info_.joints.size(), 0.0);

  return hardware_interface::CallbackReturn::SUCCESS;
}

std::vector<hardware_interface::StateInterface>
RobotHardware::export_state_interfaces()
{
  std::vector<hardware_interface::StateInterface> interfaces;

  for (std::size_t i = 0; i < info_.joints.size(); i++)
  {
    interfaces.emplace_back(
      info_.joints[i].name,
      hardware_interface::HW_IF_POSITION,
      &positions_[i]);
  }

  return interfaces;
}


std::vector<hardware_interface::CommandInterface>
RobotHardware::export_command_interfaces()
{
  std::vector<hardware_interface::CommandInterface> interfaces;

  for (std::size_t i = 0; i < info_.joints.size(); i++)
  {
    interfaces.emplace_back(
      info_.joints[i].name,
      hardware_interface::HW_IF_POSITION,
      &commands_[i]);
  }

  return interfaces;
}
}