// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from action_interfaces:msg/MagneticSpherical.idl
// generated code does not contain a copyright notice

#ifndef ACTION_INTERFACES__MSG__DETAIL__MAGNETIC_SPHERICAL__BUILDER_HPP_
#define ACTION_INTERFACES__MSG__DETAIL__MAGNETIC_SPHERICAL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "action_interfaces/msg/detail/magnetic_spherical__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace action_interfaces
{

namespace msg
{

namespace builder
{

class Init_MagneticSpherical_magnetic_field_spherical
{
public:
  Init_MagneticSpherical_magnetic_field_spherical()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::action_interfaces::msg::MagneticSpherical magnetic_field_spherical(::action_interfaces::msg::MagneticSpherical::_magnetic_field_spherical_type arg)
  {
    msg_.magnetic_field_spherical = std::move(arg);
    return std::move(msg_);
  }

private:
  ::action_interfaces::msg::MagneticSpherical msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::action_interfaces::msg::MagneticSpherical>()
{
  return action_interfaces::msg::builder::Init_MagneticSpherical_magnetic_field_spherical();
}

}  // namespace action_interfaces

#endif  // ACTION_INTERFACES__MSG__DETAIL__MAGNETIC_SPHERICAL__BUILDER_HPP_
