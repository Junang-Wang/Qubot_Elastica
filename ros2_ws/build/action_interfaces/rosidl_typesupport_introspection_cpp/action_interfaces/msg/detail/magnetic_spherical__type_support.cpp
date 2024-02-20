// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from action_interfaces:msg/MagneticSpherical.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "action_interfaces/msg/detail/magnetic_spherical__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace action_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void MagneticSpherical_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) action_interfaces::msg::MagneticSpherical(_init);
}

void MagneticSpherical_fini_function(void * message_memory)
{
  auto typed_message = static_cast<action_interfaces::msg::MagneticSpherical *>(message_memory);
  typed_message->~MagneticSpherical();
}

size_t size_function__MagneticSpherical__magnetic_field_spherical(const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * get_const_function__MagneticSpherical__magnetic_field_spherical(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void * get_function__MagneticSpherical__magnetic_field_spherical(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void fetch_function__MagneticSpherical__magnetic_field_spherical(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__MagneticSpherical__magnetic_field_spherical(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__MagneticSpherical__magnetic_field_spherical(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__MagneticSpherical__magnetic_field_spherical(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember MagneticSpherical_message_member_array[1] = {
  {
    "magnetic_field_spherical",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(action_interfaces::msg::MagneticSpherical, magnetic_field_spherical),  // bytes offset in struct
    nullptr,  // default value
    size_function__MagneticSpherical__magnetic_field_spherical,  // size() function pointer
    get_const_function__MagneticSpherical__magnetic_field_spherical,  // get_const(index) function pointer
    get_function__MagneticSpherical__magnetic_field_spherical,  // get(index) function pointer
    fetch_function__MagneticSpherical__magnetic_field_spherical,  // fetch(index, &value) function pointer
    assign_function__MagneticSpherical__magnetic_field_spherical,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers MagneticSpherical_message_members = {
  "action_interfaces::msg",  // message namespace
  "MagneticSpherical",  // message name
  1,  // number of fields
  sizeof(action_interfaces::msg::MagneticSpherical),
  MagneticSpherical_message_member_array,  // message members
  MagneticSpherical_init_function,  // function to initialize message memory (memory has to be allocated)
  MagneticSpherical_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t MagneticSpherical_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &MagneticSpherical_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace action_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<action_interfaces::msg::MagneticSpherical>()
{
  return &::action_interfaces::msg::rosidl_typesupport_introspection_cpp::MagneticSpherical_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, action_interfaces, msg, MagneticSpherical)() {
  return &::action_interfaces::msg::rosidl_typesupport_introspection_cpp::MagneticSpherical_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
