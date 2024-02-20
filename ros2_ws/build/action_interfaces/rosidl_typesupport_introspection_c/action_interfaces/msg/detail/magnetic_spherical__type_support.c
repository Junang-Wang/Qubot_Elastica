// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from action_interfaces:msg/MagneticSpherical.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "action_interfaces/msg/detail/magnetic_spherical__rosidl_typesupport_introspection_c.h"
#include "action_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "action_interfaces/msg/detail/magnetic_spherical__functions.h"
#include "action_interfaces/msg/detail/magnetic_spherical__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__MagneticSpherical_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  action_interfaces__msg__MagneticSpherical__init(message_memory);
}

void action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__MagneticSpherical_fini_function(void * message_memory)
{
  action_interfaces__msg__MagneticSpherical__fini(message_memory);
}

size_t action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__size_function__MagneticSpherical__magnetic_field_spherical(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__get_const_function__MagneticSpherical__magnetic_field_spherical(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__get_function__MagneticSpherical__magnetic_field_spherical(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__fetch_function__MagneticSpherical__magnetic_field_spherical(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__get_const_function__MagneticSpherical__magnetic_field_spherical(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__assign_function__MagneticSpherical__magnetic_field_spherical(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__get_function__MagneticSpherical__magnetic_field_spherical(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__MagneticSpherical_message_member_array[1] = {
  {
    "magnetic_field_spherical",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(action_interfaces__msg__MagneticSpherical, magnetic_field_spherical),  // bytes offset in struct
    NULL,  // default value
    action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__size_function__MagneticSpherical__magnetic_field_spherical,  // size() function pointer
    action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__get_const_function__MagneticSpherical__magnetic_field_spherical,  // get_const(index) function pointer
    action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__get_function__MagneticSpherical__magnetic_field_spherical,  // get(index) function pointer
    action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__fetch_function__MagneticSpherical__magnetic_field_spherical,  // fetch(index, &value) function pointer
    action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__assign_function__MagneticSpherical__magnetic_field_spherical,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__MagneticSpherical_message_members = {
  "action_interfaces__msg",  // message namespace
  "MagneticSpherical",  // message name
  1,  // number of fields
  sizeof(action_interfaces__msg__MagneticSpherical),
  action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__MagneticSpherical_message_member_array,  // message members
  action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__MagneticSpherical_init_function,  // function to initialize message memory (memory has to be allocated)
  action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__MagneticSpherical_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__MagneticSpherical_message_type_support_handle = {
  0,
  &action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__MagneticSpherical_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_action_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, action_interfaces, msg, MagneticSpherical)() {
  if (!action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__MagneticSpherical_message_type_support_handle.typesupport_identifier) {
    action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__MagneticSpherical_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &action_interfaces__msg__MagneticSpherical__rosidl_typesupport_introspection_c__MagneticSpherical_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
