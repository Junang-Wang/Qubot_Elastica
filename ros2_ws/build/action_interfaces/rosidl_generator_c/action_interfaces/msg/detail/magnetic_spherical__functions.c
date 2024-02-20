// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from action_interfaces:msg/MagneticSpherical.idl
// generated code does not contain a copyright notice
#include "action_interfaces/msg/detail/magnetic_spherical__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
action_interfaces__msg__MagneticSpherical__init(action_interfaces__msg__MagneticSpherical * msg)
{
  if (!msg) {
    return false;
  }
  // magnetic_field_spherical
  return true;
}

void
action_interfaces__msg__MagneticSpherical__fini(action_interfaces__msg__MagneticSpherical * msg)
{
  if (!msg) {
    return;
  }
  // magnetic_field_spherical
}

bool
action_interfaces__msg__MagneticSpherical__are_equal(const action_interfaces__msg__MagneticSpherical * lhs, const action_interfaces__msg__MagneticSpherical * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // magnetic_field_spherical
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->magnetic_field_spherical[i] != rhs->magnetic_field_spherical[i]) {
      return false;
    }
  }
  return true;
}

bool
action_interfaces__msg__MagneticSpherical__copy(
  const action_interfaces__msg__MagneticSpherical * input,
  action_interfaces__msg__MagneticSpherical * output)
{
  if (!input || !output) {
    return false;
  }
  // magnetic_field_spherical
  for (size_t i = 0; i < 3; ++i) {
    output->magnetic_field_spherical[i] = input->magnetic_field_spherical[i];
  }
  return true;
}

action_interfaces__msg__MagneticSpherical *
action_interfaces__msg__MagneticSpherical__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__msg__MagneticSpherical * msg = (action_interfaces__msg__MagneticSpherical *)allocator.allocate(sizeof(action_interfaces__msg__MagneticSpherical), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(action_interfaces__msg__MagneticSpherical));
  bool success = action_interfaces__msg__MagneticSpherical__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
action_interfaces__msg__MagneticSpherical__destroy(action_interfaces__msg__MagneticSpherical * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    action_interfaces__msg__MagneticSpherical__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
action_interfaces__msg__MagneticSpherical__Sequence__init(action_interfaces__msg__MagneticSpherical__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__msg__MagneticSpherical * data = NULL;

  if (size) {
    data = (action_interfaces__msg__MagneticSpherical *)allocator.zero_allocate(size, sizeof(action_interfaces__msg__MagneticSpherical), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = action_interfaces__msg__MagneticSpherical__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        action_interfaces__msg__MagneticSpherical__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
action_interfaces__msg__MagneticSpherical__Sequence__fini(action_interfaces__msg__MagneticSpherical__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      action_interfaces__msg__MagneticSpherical__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

action_interfaces__msg__MagneticSpherical__Sequence *
action_interfaces__msg__MagneticSpherical__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__msg__MagneticSpherical__Sequence * array = (action_interfaces__msg__MagneticSpherical__Sequence *)allocator.allocate(sizeof(action_interfaces__msg__MagneticSpherical__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = action_interfaces__msg__MagneticSpherical__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
action_interfaces__msg__MagneticSpherical__Sequence__destroy(action_interfaces__msg__MagneticSpherical__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    action_interfaces__msg__MagneticSpherical__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
action_interfaces__msg__MagneticSpherical__Sequence__are_equal(const action_interfaces__msg__MagneticSpherical__Sequence * lhs, const action_interfaces__msg__MagneticSpherical__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!action_interfaces__msg__MagneticSpherical__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
action_interfaces__msg__MagneticSpherical__Sequence__copy(
  const action_interfaces__msg__MagneticSpherical__Sequence * input,
  action_interfaces__msg__MagneticSpherical__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(action_interfaces__msg__MagneticSpherical);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    action_interfaces__msg__MagneticSpherical * data =
      (action_interfaces__msg__MagneticSpherical *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!action_interfaces__msg__MagneticSpherical__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          action_interfaces__msg__MagneticSpherical__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!action_interfaces__msg__MagneticSpherical__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
