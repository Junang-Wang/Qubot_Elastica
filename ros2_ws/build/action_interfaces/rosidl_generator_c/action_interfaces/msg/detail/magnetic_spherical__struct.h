// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from action_interfaces:msg/MagneticSpherical.idl
// generated code does not contain a copyright notice

#ifndef ACTION_INTERFACES__MSG__DETAIL__MAGNETIC_SPHERICAL__STRUCT_H_
#define ACTION_INTERFACES__MSG__DETAIL__MAGNETIC_SPHERICAL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/MagneticSpherical in the package action_interfaces.
typedef struct action_interfaces__msg__MagneticSpherical
{
  double magnetic_field_spherical[3];
} action_interfaces__msg__MagneticSpherical;

// Struct for a sequence of action_interfaces__msg__MagneticSpherical.
typedef struct action_interfaces__msg__MagneticSpherical__Sequence
{
  action_interfaces__msg__MagneticSpherical * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} action_interfaces__msg__MagneticSpherical__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ACTION_INTERFACES__MSG__DETAIL__MAGNETIC_SPHERICAL__STRUCT_H_
