// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from action_interfaces:action/CountUntil.idl
// generated code does not contain a copyright notice
#include "action_interfaces/action/detail/count_until__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
action_interfaces__action__CountUntil_Goal__init(action_interfaces__action__CountUntil_Goal * msg)
{
  if (!msg) {
    return false;
  }
  // target_number
  // period
  return true;
}

void
action_interfaces__action__CountUntil_Goal__fini(action_interfaces__action__CountUntil_Goal * msg)
{
  if (!msg) {
    return;
  }
  // target_number
  // period
}

bool
action_interfaces__action__CountUntil_Goal__are_equal(const action_interfaces__action__CountUntil_Goal * lhs, const action_interfaces__action__CountUntil_Goal * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // target_number
  if (lhs->target_number != rhs->target_number) {
    return false;
  }
  // period
  if (lhs->period != rhs->period) {
    return false;
  }
  return true;
}

bool
action_interfaces__action__CountUntil_Goal__copy(
  const action_interfaces__action__CountUntil_Goal * input,
  action_interfaces__action__CountUntil_Goal * output)
{
  if (!input || !output) {
    return false;
  }
  // target_number
  output->target_number = input->target_number;
  // period
  output->period = input->period;
  return true;
}

action_interfaces__action__CountUntil_Goal *
action_interfaces__action__CountUntil_Goal__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_Goal * msg = (action_interfaces__action__CountUntil_Goal *)allocator.allocate(sizeof(action_interfaces__action__CountUntil_Goal), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(action_interfaces__action__CountUntil_Goal));
  bool success = action_interfaces__action__CountUntil_Goal__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
action_interfaces__action__CountUntil_Goal__destroy(action_interfaces__action__CountUntil_Goal * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    action_interfaces__action__CountUntil_Goal__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
action_interfaces__action__CountUntil_Goal__Sequence__init(action_interfaces__action__CountUntil_Goal__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_Goal * data = NULL;

  if (size) {
    data = (action_interfaces__action__CountUntil_Goal *)allocator.zero_allocate(size, sizeof(action_interfaces__action__CountUntil_Goal), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = action_interfaces__action__CountUntil_Goal__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        action_interfaces__action__CountUntil_Goal__fini(&data[i - 1]);
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
action_interfaces__action__CountUntil_Goal__Sequence__fini(action_interfaces__action__CountUntil_Goal__Sequence * array)
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
      action_interfaces__action__CountUntil_Goal__fini(&array->data[i]);
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

action_interfaces__action__CountUntil_Goal__Sequence *
action_interfaces__action__CountUntil_Goal__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_Goal__Sequence * array = (action_interfaces__action__CountUntil_Goal__Sequence *)allocator.allocate(sizeof(action_interfaces__action__CountUntil_Goal__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = action_interfaces__action__CountUntil_Goal__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
action_interfaces__action__CountUntil_Goal__Sequence__destroy(action_interfaces__action__CountUntil_Goal__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    action_interfaces__action__CountUntil_Goal__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
action_interfaces__action__CountUntil_Goal__Sequence__are_equal(const action_interfaces__action__CountUntil_Goal__Sequence * lhs, const action_interfaces__action__CountUntil_Goal__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!action_interfaces__action__CountUntil_Goal__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
action_interfaces__action__CountUntil_Goal__Sequence__copy(
  const action_interfaces__action__CountUntil_Goal__Sequence * input,
  action_interfaces__action__CountUntil_Goal__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(action_interfaces__action__CountUntil_Goal);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    action_interfaces__action__CountUntil_Goal * data =
      (action_interfaces__action__CountUntil_Goal *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!action_interfaces__action__CountUntil_Goal__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          action_interfaces__action__CountUntil_Goal__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!action_interfaces__action__CountUntil_Goal__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
action_interfaces__action__CountUntil_Result__init(action_interfaces__action__CountUntil_Result * msg)
{
  if (!msg) {
    return false;
  }
  // reached_number
  return true;
}

void
action_interfaces__action__CountUntil_Result__fini(action_interfaces__action__CountUntil_Result * msg)
{
  if (!msg) {
    return;
  }
  // reached_number
}

bool
action_interfaces__action__CountUntil_Result__are_equal(const action_interfaces__action__CountUntil_Result * lhs, const action_interfaces__action__CountUntil_Result * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // reached_number
  if (lhs->reached_number != rhs->reached_number) {
    return false;
  }
  return true;
}

bool
action_interfaces__action__CountUntil_Result__copy(
  const action_interfaces__action__CountUntil_Result * input,
  action_interfaces__action__CountUntil_Result * output)
{
  if (!input || !output) {
    return false;
  }
  // reached_number
  output->reached_number = input->reached_number;
  return true;
}

action_interfaces__action__CountUntil_Result *
action_interfaces__action__CountUntil_Result__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_Result * msg = (action_interfaces__action__CountUntil_Result *)allocator.allocate(sizeof(action_interfaces__action__CountUntil_Result), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(action_interfaces__action__CountUntil_Result));
  bool success = action_interfaces__action__CountUntil_Result__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
action_interfaces__action__CountUntil_Result__destroy(action_interfaces__action__CountUntil_Result * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    action_interfaces__action__CountUntil_Result__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
action_interfaces__action__CountUntil_Result__Sequence__init(action_interfaces__action__CountUntil_Result__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_Result * data = NULL;

  if (size) {
    data = (action_interfaces__action__CountUntil_Result *)allocator.zero_allocate(size, sizeof(action_interfaces__action__CountUntil_Result), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = action_interfaces__action__CountUntil_Result__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        action_interfaces__action__CountUntil_Result__fini(&data[i - 1]);
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
action_interfaces__action__CountUntil_Result__Sequence__fini(action_interfaces__action__CountUntil_Result__Sequence * array)
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
      action_interfaces__action__CountUntil_Result__fini(&array->data[i]);
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

action_interfaces__action__CountUntil_Result__Sequence *
action_interfaces__action__CountUntil_Result__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_Result__Sequence * array = (action_interfaces__action__CountUntil_Result__Sequence *)allocator.allocate(sizeof(action_interfaces__action__CountUntil_Result__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = action_interfaces__action__CountUntil_Result__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
action_interfaces__action__CountUntil_Result__Sequence__destroy(action_interfaces__action__CountUntil_Result__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    action_interfaces__action__CountUntil_Result__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
action_interfaces__action__CountUntil_Result__Sequence__are_equal(const action_interfaces__action__CountUntil_Result__Sequence * lhs, const action_interfaces__action__CountUntil_Result__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!action_interfaces__action__CountUntil_Result__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
action_interfaces__action__CountUntil_Result__Sequence__copy(
  const action_interfaces__action__CountUntil_Result__Sequence * input,
  action_interfaces__action__CountUntil_Result__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(action_interfaces__action__CountUntil_Result);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    action_interfaces__action__CountUntil_Result * data =
      (action_interfaces__action__CountUntil_Result *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!action_interfaces__action__CountUntil_Result__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          action_interfaces__action__CountUntil_Result__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!action_interfaces__action__CountUntil_Result__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
action_interfaces__action__CountUntil_Feedback__init(action_interfaces__action__CountUntil_Feedback * msg)
{
  if (!msg) {
    return false;
  }
  // current_number
  return true;
}

void
action_interfaces__action__CountUntil_Feedback__fini(action_interfaces__action__CountUntil_Feedback * msg)
{
  if (!msg) {
    return;
  }
  // current_number
}

bool
action_interfaces__action__CountUntil_Feedback__are_equal(const action_interfaces__action__CountUntil_Feedback * lhs, const action_interfaces__action__CountUntil_Feedback * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // current_number
  if (lhs->current_number != rhs->current_number) {
    return false;
  }
  return true;
}

bool
action_interfaces__action__CountUntil_Feedback__copy(
  const action_interfaces__action__CountUntil_Feedback * input,
  action_interfaces__action__CountUntil_Feedback * output)
{
  if (!input || !output) {
    return false;
  }
  // current_number
  output->current_number = input->current_number;
  return true;
}

action_interfaces__action__CountUntil_Feedback *
action_interfaces__action__CountUntil_Feedback__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_Feedback * msg = (action_interfaces__action__CountUntil_Feedback *)allocator.allocate(sizeof(action_interfaces__action__CountUntil_Feedback), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(action_interfaces__action__CountUntil_Feedback));
  bool success = action_interfaces__action__CountUntil_Feedback__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
action_interfaces__action__CountUntil_Feedback__destroy(action_interfaces__action__CountUntil_Feedback * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    action_interfaces__action__CountUntil_Feedback__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
action_interfaces__action__CountUntil_Feedback__Sequence__init(action_interfaces__action__CountUntil_Feedback__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_Feedback * data = NULL;

  if (size) {
    data = (action_interfaces__action__CountUntil_Feedback *)allocator.zero_allocate(size, sizeof(action_interfaces__action__CountUntil_Feedback), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = action_interfaces__action__CountUntil_Feedback__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        action_interfaces__action__CountUntil_Feedback__fini(&data[i - 1]);
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
action_interfaces__action__CountUntil_Feedback__Sequence__fini(action_interfaces__action__CountUntil_Feedback__Sequence * array)
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
      action_interfaces__action__CountUntil_Feedback__fini(&array->data[i]);
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

action_interfaces__action__CountUntil_Feedback__Sequence *
action_interfaces__action__CountUntil_Feedback__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_Feedback__Sequence * array = (action_interfaces__action__CountUntil_Feedback__Sequence *)allocator.allocate(sizeof(action_interfaces__action__CountUntil_Feedback__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = action_interfaces__action__CountUntil_Feedback__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
action_interfaces__action__CountUntil_Feedback__Sequence__destroy(action_interfaces__action__CountUntil_Feedback__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    action_interfaces__action__CountUntil_Feedback__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
action_interfaces__action__CountUntil_Feedback__Sequence__are_equal(const action_interfaces__action__CountUntil_Feedback__Sequence * lhs, const action_interfaces__action__CountUntil_Feedback__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!action_interfaces__action__CountUntil_Feedback__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
action_interfaces__action__CountUntil_Feedback__Sequence__copy(
  const action_interfaces__action__CountUntil_Feedback__Sequence * input,
  action_interfaces__action__CountUntil_Feedback__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(action_interfaces__action__CountUntil_Feedback);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    action_interfaces__action__CountUntil_Feedback * data =
      (action_interfaces__action__CountUntil_Feedback *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!action_interfaces__action__CountUntil_Feedback__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          action_interfaces__action__CountUntil_Feedback__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!action_interfaces__action__CountUntil_Feedback__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
#include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `goal`
// already included above
// #include "action_interfaces/action/detail/count_until__functions.h"

bool
action_interfaces__action__CountUntil_SendGoal_Request__init(action_interfaces__action__CountUntil_SendGoal_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    action_interfaces__action__CountUntil_SendGoal_Request__fini(msg);
    return false;
  }
  // goal
  if (!action_interfaces__action__CountUntil_Goal__init(&msg->goal)) {
    action_interfaces__action__CountUntil_SendGoal_Request__fini(msg);
    return false;
  }
  return true;
}

void
action_interfaces__action__CountUntil_SendGoal_Request__fini(action_interfaces__action__CountUntil_SendGoal_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // goal
  action_interfaces__action__CountUntil_Goal__fini(&msg->goal);
}

bool
action_interfaces__action__CountUntil_SendGoal_Request__are_equal(const action_interfaces__action__CountUntil_SendGoal_Request * lhs, const action_interfaces__action__CountUntil_SendGoal_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // goal
  if (!action_interfaces__action__CountUntil_Goal__are_equal(
      &(lhs->goal), &(rhs->goal)))
  {
    return false;
  }
  return true;
}

bool
action_interfaces__action__CountUntil_SendGoal_Request__copy(
  const action_interfaces__action__CountUntil_SendGoal_Request * input,
  action_interfaces__action__CountUntil_SendGoal_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // goal
  if (!action_interfaces__action__CountUntil_Goal__copy(
      &(input->goal), &(output->goal)))
  {
    return false;
  }
  return true;
}

action_interfaces__action__CountUntil_SendGoal_Request *
action_interfaces__action__CountUntil_SendGoal_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_SendGoal_Request * msg = (action_interfaces__action__CountUntil_SendGoal_Request *)allocator.allocate(sizeof(action_interfaces__action__CountUntil_SendGoal_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(action_interfaces__action__CountUntil_SendGoal_Request));
  bool success = action_interfaces__action__CountUntil_SendGoal_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
action_interfaces__action__CountUntil_SendGoal_Request__destroy(action_interfaces__action__CountUntil_SendGoal_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    action_interfaces__action__CountUntil_SendGoal_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
action_interfaces__action__CountUntil_SendGoal_Request__Sequence__init(action_interfaces__action__CountUntil_SendGoal_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_SendGoal_Request * data = NULL;

  if (size) {
    data = (action_interfaces__action__CountUntil_SendGoal_Request *)allocator.zero_allocate(size, sizeof(action_interfaces__action__CountUntil_SendGoal_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = action_interfaces__action__CountUntil_SendGoal_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        action_interfaces__action__CountUntil_SendGoal_Request__fini(&data[i - 1]);
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
action_interfaces__action__CountUntil_SendGoal_Request__Sequence__fini(action_interfaces__action__CountUntil_SendGoal_Request__Sequence * array)
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
      action_interfaces__action__CountUntil_SendGoal_Request__fini(&array->data[i]);
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

action_interfaces__action__CountUntil_SendGoal_Request__Sequence *
action_interfaces__action__CountUntil_SendGoal_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_SendGoal_Request__Sequence * array = (action_interfaces__action__CountUntil_SendGoal_Request__Sequence *)allocator.allocate(sizeof(action_interfaces__action__CountUntil_SendGoal_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = action_interfaces__action__CountUntil_SendGoal_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
action_interfaces__action__CountUntil_SendGoal_Request__Sequence__destroy(action_interfaces__action__CountUntil_SendGoal_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    action_interfaces__action__CountUntil_SendGoal_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
action_interfaces__action__CountUntil_SendGoal_Request__Sequence__are_equal(const action_interfaces__action__CountUntil_SendGoal_Request__Sequence * lhs, const action_interfaces__action__CountUntil_SendGoal_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!action_interfaces__action__CountUntil_SendGoal_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
action_interfaces__action__CountUntil_SendGoal_Request__Sequence__copy(
  const action_interfaces__action__CountUntil_SendGoal_Request__Sequence * input,
  action_interfaces__action__CountUntil_SendGoal_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(action_interfaces__action__CountUntil_SendGoal_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    action_interfaces__action__CountUntil_SendGoal_Request * data =
      (action_interfaces__action__CountUntil_SendGoal_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!action_interfaces__action__CountUntil_SendGoal_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          action_interfaces__action__CountUntil_SendGoal_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!action_interfaces__action__CountUntil_SendGoal_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
action_interfaces__action__CountUntil_SendGoal_Response__init(action_interfaces__action__CountUntil_SendGoal_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    action_interfaces__action__CountUntil_SendGoal_Response__fini(msg);
    return false;
  }
  return true;
}

void
action_interfaces__action__CountUntil_SendGoal_Response__fini(action_interfaces__action__CountUntil_SendGoal_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
}

bool
action_interfaces__action__CountUntil_SendGoal_Response__are_equal(const action_interfaces__action__CountUntil_SendGoal_Response * lhs, const action_interfaces__action__CountUntil_SendGoal_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // accepted
  if (lhs->accepted != rhs->accepted) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->stamp), &(rhs->stamp)))
  {
    return false;
  }
  return true;
}

bool
action_interfaces__action__CountUntil_SendGoal_Response__copy(
  const action_interfaces__action__CountUntil_SendGoal_Response * input,
  action_interfaces__action__CountUntil_SendGoal_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // accepted
  output->accepted = input->accepted;
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  return true;
}

action_interfaces__action__CountUntil_SendGoal_Response *
action_interfaces__action__CountUntil_SendGoal_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_SendGoal_Response * msg = (action_interfaces__action__CountUntil_SendGoal_Response *)allocator.allocate(sizeof(action_interfaces__action__CountUntil_SendGoal_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(action_interfaces__action__CountUntil_SendGoal_Response));
  bool success = action_interfaces__action__CountUntil_SendGoal_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
action_interfaces__action__CountUntil_SendGoal_Response__destroy(action_interfaces__action__CountUntil_SendGoal_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    action_interfaces__action__CountUntil_SendGoal_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
action_interfaces__action__CountUntil_SendGoal_Response__Sequence__init(action_interfaces__action__CountUntil_SendGoal_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_SendGoal_Response * data = NULL;

  if (size) {
    data = (action_interfaces__action__CountUntil_SendGoal_Response *)allocator.zero_allocate(size, sizeof(action_interfaces__action__CountUntil_SendGoal_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = action_interfaces__action__CountUntil_SendGoal_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        action_interfaces__action__CountUntil_SendGoal_Response__fini(&data[i - 1]);
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
action_interfaces__action__CountUntil_SendGoal_Response__Sequence__fini(action_interfaces__action__CountUntil_SendGoal_Response__Sequence * array)
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
      action_interfaces__action__CountUntil_SendGoal_Response__fini(&array->data[i]);
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

action_interfaces__action__CountUntil_SendGoal_Response__Sequence *
action_interfaces__action__CountUntil_SendGoal_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_SendGoal_Response__Sequence * array = (action_interfaces__action__CountUntil_SendGoal_Response__Sequence *)allocator.allocate(sizeof(action_interfaces__action__CountUntil_SendGoal_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = action_interfaces__action__CountUntil_SendGoal_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
action_interfaces__action__CountUntil_SendGoal_Response__Sequence__destroy(action_interfaces__action__CountUntil_SendGoal_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    action_interfaces__action__CountUntil_SendGoal_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
action_interfaces__action__CountUntil_SendGoal_Response__Sequence__are_equal(const action_interfaces__action__CountUntil_SendGoal_Response__Sequence * lhs, const action_interfaces__action__CountUntil_SendGoal_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!action_interfaces__action__CountUntil_SendGoal_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
action_interfaces__action__CountUntil_SendGoal_Response__Sequence__copy(
  const action_interfaces__action__CountUntil_SendGoal_Response__Sequence * input,
  action_interfaces__action__CountUntil_SendGoal_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(action_interfaces__action__CountUntil_SendGoal_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    action_interfaces__action__CountUntil_SendGoal_Response * data =
      (action_interfaces__action__CountUntil_SendGoal_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!action_interfaces__action__CountUntil_SendGoal_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          action_interfaces__action__CountUntil_SendGoal_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!action_interfaces__action__CountUntil_SendGoal_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"

bool
action_interfaces__action__CountUntil_GetResult_Request__init(action_interfaces__action__CountUntil_GetResult_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    action_interfaces__action__CountUntil_GetResult_Request__fini(msg);
    return false;
  }
  return true;
}

void
action_interfaces__action__CountUntil_GetResult_Request__fini(action_interfaces__action__CountUntil_GetResult_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
}

bool
action_interfaces__action__CountUntil_GetResult_Request__are_equal(const action_interfaces__action__CountUntil_GetResult_Request * lhs, const action_interfaces__action__CountUntil_GetResult_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  return true;
}

bool
action_interfaces__action__CountUntil_GetResult_Request__copy(
  const action_interfaces__action__CountUntil_GetResult_Request * input,
  action_interfaces__action__CountUntil_GetResult_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  return true;
}

action_interfaces__action__CountUntil_GetResult_Request *
action_interfaces__action__CountUntil_GetResult_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_GetResult_Request * msg = (action_interfaces__action__CountUntil_GetResult_Request *)allocator.allocate(sizeof(action_interfaces__action__CountUntil_GetResult_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(action_interfaces__action__CountUntil_GetResult_Request));
  bool success = action_interfaces__action__CountUntil_GetResult_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
action_interfaces__action__CountUntil_GetResult_Request__destroy(action_interfaces__action__CountUntil_GetResult_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    action_interfaces__action__CountUntil_GetResult_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
action_interfaces__action__CountUntil_GetResult_Request__Sequence__init(action_interfaces__action__CountUntil_GetResult_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_GetResult_Request * data = NULL;

  if (size) {
    data = (action_interfaces__action__CountUntil_GetResult_Request *)allocator.zero_allocate(size, sizeof(action_interfaces__action__CountUntil_GetResult_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = action_interfaces__action__CountUntil_GetResult_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        action_interfaces__action__CountUntil_GetResult_Request__fini(&data[i - 1]);
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
action_interfaces__action__CountUntil_GetResult_Request__Sequence__fini(action_interfaces__action__CountUntil_GetResult_Request__Sequence * array)
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
      action_interfaces__action__CountUntil_GetResult_Request__fini(&array->data[i]);
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

action_interfaces__action__CountUntil_GetResult_Request__Sequence *
action_interfaces__action__CountUntil_GetResult_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_GetResult_Request__Sequence * array = (action_interfaces__action__CountUntil_GetResult_Request__Sequence *)allocator.allocate(sizeof(action_interfaces__action__CountUntil_GetResult_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = action_interfaces__action__CountUntil_GetResult_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
action_interfaces__action__CountUntil_GetResult_Request__Sequence__destroy(action_interfaces__action__CountUntil_GetResult_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    action_interfaces__action__CountUntil_GetResult_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
action_interfaces__action__CountUntil_GetResult_Request__Sequence__are_equal(const action_interfaces__action__CountUntil_GetResult_Request__Sequence * lhs, const action_interfaces__action__CountUntil_GetResult_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!action_interfaces__action__CountUntil_GetResult_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
action_interfaces__action__CountUntil_GetResult_Request__Sequence__copy(
  const action_interfaces__action__CountUntil_GetResult_Request__Sequence * input,
  action_interfaces__action__CountUntil_GetResult_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(action_interfaces__action__CountUntil_GetResult_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    action_interfaces__action__CountUntil_GetResult_Request * data =
      (action_interfaces__action__CountUntil_GetResult_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!action_interfaces__action__CountUntil_GetResult_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          action_interfaces__action__CountUntil_GetResult_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!action_interfaces__action__CountUntil_GetResult_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `result`
// already included above
// #include "action_interfaces/action/detail/count_until__functions.h"

bool
action_interfaces__action__CountUntil_GetResult_Response__init(action_interfaces__action__CountUntil_GetResult_Response * msg)
{
  if (!msg) {
    return false;
  }
  // status
  // result
  if (!action_interfaces__action__CountUntil_Result__init(&msg->result)) {
    action_interfaces__action__CountUntil_GetResult_Response__fini(msg);
    return false;
  }
  return true;
}

void
action_interfaces__action__CountUntil_GetResult_Response__fini(action_interfaces__action__CountUntil_GetResult_Response * msg)
{
  if (!msg) {
    return;
  }
  // status
  // result
  action_interfaces__action__CountUntil_Result__fini(&msg->result);
}

bool
action_interfaces__action__CountUntil_GetResult_Response__are_equal(const action_interfaces__action__CountUntil_GetResult_Response * lhs, const action_interfaces__action__CountUntil_GetResult_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  // result
  if (!action_interfaces__action__CountUntil_Result__are_equal(
      &(lhs->result), &(rhs->result)))
  {
    return false;
  }
  return true;
}

bool
action_interfaces__action__CountUntil_GetResult_Response__copy(
  const action_interfaces__action__CountUntil_GetResult_Response * input,
  action_interfaces__action__CountUntil_GetResult_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  // result
  if (!action_interfaces__action__CountUntil_Result__copy(
      &(input->result), &(output->result)))
  {
    return false;
  }
  return true;
}

action_interfaces__action__CountUntil_GetResult_Response *
action_interfaces__action__CountUntil_GetResult_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_GetResult_Response * msg = (action_interfaces__action__CountUntil_GetResult_Response *)allocator.allocate(sizeof(action_interfaces__action__CountUntil_GetResult_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(action_interfaces__action__CountUntil_GetResult_Response));
  bool success = action_interfaces__action__CountUntil_GetResult_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
action_interfaces__action__CountUntil_GetResult_Response__destroy(action_interfaces__action__CountUntil_GetResult_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    action_interfaces__action__CountUntil_GetResult_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
action_interfaces__action__CountUntil_GetResult_Response__Sequence__init(action_interfaces__action__CountUntil_GetResult_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_GetResult_Response * data = NULL;

  if (size) {
    data = (action_interfaces__action__CountUntil_GetResult_Response *)allocator.zero_allocate(size, sizeof(action_interfaces__action__CountUntil_GetResult_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = action_interfaces__action__CountUntil_GetResult_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        action_interfaces__action__CountUntil_GetResult_Response__fini(&data[i - 1]);
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
action_interfaces__action__CountUntil_GetResult_Response__Sequence__fini(action_interfaces__action__CountUntil_GetResult_Response__Sequence * array)
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
      action_interfaces__action__CountUntil_GetResult_Response__fini(&array->data[i]);
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

action_interfaces__action__CountUntil_GetResult_Response__Sequence *
action_interfaces__action__CountUntil_GetResult_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_GetResult_Response__Sequence * array = (action_interfaces__action__CountUntil_GetResult_Response__Sequence *)allocator.allocate(sizeof(action_interfaces__action__CountUntil_GetResult_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = action_interfaces__action__CountUntil_GetResult_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
action_interfaces__action__CountUntil_GetResult_Response__Sequence__destroy(action_interfaces__action__CountUntil_GetResult_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    action_interfaces__action__CountUntil_GetResult_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
action_interfaces__action__CountUntil_GetResult_Response__Sequence__are_equal(const action_interfaces__action__CountUntil_GetResult_Response__Sequence * lhs, const action_interfaces__action__CountUntil_GetResult_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!action_interfaces__action__CountUntil_GetResult_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
action_interfaces__action__CountUntil_GetResult_Response__Sequence__copy(
  const action_interfaces__action__CountUntil_GetResult_Response__Sequence * input,
  action_interfaces__action__CountUntil_GetResult_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(action_interfaces__action__CountUntil_GetResult_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    action_interfaces__action__CountUntil_GetResult_Response * data =
      (action_interfaces__action__CountUntil_GetResult_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!action_interfaces__action__CountUntil_GetResult_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          action_interfaces__action__CountUntil_GetResult_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!action_interfaces__action__CountUntil_GetResult_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `feedback`
// already included above
// #include "action_interfaces/action/detail/count_until__functions.h"

bool
action_interfaces__action__CountUntil_FeedbackMessage__init(action_interfaces__action__CountUntil_FeedbackMessage * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    action_interfaces__action__CountUntil_FeedbackMessage__fini(msg);
    return false;
  }
  // feedback
  if (!action_interfaces__action__CountUntil_Feedback__init(&msg->feedback)) {
    action_interfaces__action__CountUntil_FeedbackMessage__fini(msg);
    return false;
  }
  return true;
}

void
action_interfaces__action__CountUntil_FeedbackMessage__fini(action_interfaces__action__CountUntil_FeedbackMessage * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // feedback
  action_interfaces__action__CountUntil_Feedback__fini(&msg->feedback);
}

bool
action_interfaces__action__CountUntil_FeedbackMessage__are_equal(const action_interfaces__action__CountUntil_FeedbackMessage * lhs, const action_interfaces__action__CountUntil_FeedbackMessage * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // feedback
  if (!action_interfaces__action__CountUntil_Feedback__are_equal(
      &(lhs->feedback), &(rhs->feedback)))
  {
    return false;
  }
  return true;
}

bool
action_interfaces__action__CountUntil_FeedbackMessage__copy(
  const action_interfaces__action__CountUntil_FeedbackMessage * input,
  action_interfaces__action__CountUntil_FeedbackMessage * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // feedback
  if (!action_interfaces__action__CountUntil_Feedback__copy(
      &(input->feedback), &(output->feedback)))
  {
    return false;
  }
  return true;
}

action_interfaces__action__CountUntil_FeedbackMessage *
action_interfaces__action__CountUntil_FeedbackMessage__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_FeedbackMessage * msg = (action_interfaces__action__CountUntil_FeedbackMessage *)allocator.allocate(sizeof(action_interfaces__action__CountUntil_FeedbackMessage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(action_interfaces__action__CountUntil_FeedbackMessage));
  bool success = action_interfaces__action__CountUntil_FeedbackMessage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
action_interfaces__action__CountUntil_FeedbackMessage__destroy(action_interfaces__action__CountUntil_FeedbackMessage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    action_interfaces__action__CountUntil_FeedbackMessage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
action_interfaces__action__CountUntil_FeedbackMessage__Sequence__init(action_interfaces__action__CountUntil_FeedbackMessage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_FeedbackMessage * data = NULL;

  if (size) {
    data = (action_interfaces__action__CountUntil_FeedbackMessage *)allocator.zero_allocate(size, sizeof(action_interfaces__action__CountUntil_FeedbackMessage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = action_interfaces__action__CountUntil_FeedbackMessage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        action_interfaces__action__CountUntil_FeedbackMessage__fini(&data[i - 1]);
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
action_interfaces__action__CountUntil_FeedbackMessage__Sequence__fini(action_interfaces__action__CountUntil_FeedbackMessage__Sequence * array)
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
      action_interfaces__action__CountUntil_FeedbackMessage__fini(&array->data[i]);
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

action_interfaces__action__CountUntil_FeedbackMessage__Sequence *
action_interfaces__action__CountUntil_FeedbackMessage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  action_interfaces__action__CountUntil_FeedbackMessage__Sequence * array = (action_interfaces__action__CountUntil_FeedbackMessage__Sequence *)allocator.allocate(sizeof(action_interfaces__action__CountUntil_FeedbackMessage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = action_interfaces__action__CountUntil_FeedbackMessage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
action_interfaces__action__CountUntil_FeedbackMessage__Sequence__destroy(action_interfaces__action__CountUntil_FeedbackMessage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    action_interfaces__action__CountUntil_FeedbackMessage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
action_interfaces__action__CountUntil_FeedbackMessage__Sequence__are_equal(const action_interfaces__action__CountUntil_FeedbackMessage__Sequence * lhs, const action_interfaces__action__CountUntil_FeedbackMessage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!action_interfaces__action__CountUntil_FeedbackMessage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
action_interfaces__action__CountUntil_FeedbackMessage__Sequence__copy(
  const action_interfaces__action__CountUntil_FeedbackMessage__Sequence * input,
  action_interfaces__action__CountUntil_FeedbackMessage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(action_interfaces__action__CountUntil_FeedbackMessage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    action_interfaces__action__CountUntil_FeedbackMessage * data =
      (action_interfaces__action__CountUntil_FeedbackMessage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!action_interfaces__action__CountUntil_FeedbackMessage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          action_interfaces__action__CountUntil_FeedbackMessage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!action_interfaces__action__CountUntil_FeedbackMessage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
