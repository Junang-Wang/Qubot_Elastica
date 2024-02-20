// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from action_interfaces:msg/MagneticSpherical.idl
// generated code does not contain a copyright notice

#ifndef ACTION_INTERFACES__MSG__DETAIL__MAGNETIC_SPHERICAL__TRAITS_HPP_
#define ACTION_INTERFACES__MSG__DETAIL__MAGNETIC_SPHERICAL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "action_interfaces/msg/detail/magnetic_spherical__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace action_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const MagneticSpherical & msg,
  std::ostream & out)
{
  out << "{";
  // member: magnetic_field_spherical
  {
    if (msg.magnetic_field_spherical.size() == 0) {
      out << "magnetic_field_spherical: []";
    } else {
      out << "magnetic_field_spherical: [";
      size_t pending_items = msg.magnetic_field_spherical.size();
      for (auto item : msg.magnetic_field_spherical) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MagneticSpherical & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: magnetic_field_spherical
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.magnetic_field_spherical.size() == 0) {
      out << "magnetic_field_spherical: []\n";
    } else {
      out << "magnetic_field_spherical:\n";
      for (auto item : msg.magnetic_field_spherical) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MagneticSpherical & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace action_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use action_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const action_interfaces::msg::MagneticSpherical & msg,
  std::ostream & out, size_t indentation = 0)
{
  action_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use action_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const action_interfaces::msg::MagneticSpherical & msg)
{
  return action_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<action_interfaces::msg::MagneticSpherical>()
{
  return "action_interfaces::msg::MagneticSpherical";
}

template<>
inline const char * name<action_interfaces::msg::MagneticSpherical>()
{
  return "action_interfaces/msg/MagneticSpherical";
}

template<>
struct has_fixed_size<action_interfaces::msg::MagneticSpherical>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<action_interfaces::msg::MagneticSpherical>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<action_interfaces::msg::MagneticSpherical>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ACTION_INTERFACES__MSG__DETAIL__MAGNETIC_SPHERICAL__TRAITS_HPP_
