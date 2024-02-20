// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from action_interfaces:msg/MagneticSpherical.idl
// generated code does not contain a copyright notice

#ifndef ACTION_INTERFACES__MSG__DETAIL__MAGNETIC_SPHERICAL__STRUCT_HPP_
#define ACTION_INTERFACES__MSG__DETAIL__MAGNETIC_SPHERICAL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__action_interfaces__msg__MagneticSpherical __attribute__((deprecated))
#else
# define DEPRECATED__action_interfaces__msg__MagneticSpherical __declspec(deprecated)
#endif

namespace action_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MagneticSpherical_
{
  using Type = MagneticSpherical_<ContainerAllocator>;

  explicit MagneticSpherical_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 3>::iterator, double>(this->magnetic_field_spherical.begin(), this->magnetic_field_spherical.end(), 0.0);
    }
  }

  explicit MagneticSpherical_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : magnetic_field_spherical(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 3>::iterator, double>(this->magnetic_field_spherical.begin(), this->magnetic_field_spherical.end(), 0.0);
    }
  }

  // field types and members
  using _magnetic_field_spherical_type =
    std::array<double, 3>;
  _magnetic_field_spherical_type magnetic_field_spherical;

  // setters for named parameter idiom
  Type & set__magnetic_field_spherical(
    const std::array<double, 3> & _arg)
  {
    this->magnetic_field_spherical = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    action_interfaces::msg::MagneticSpherical_<ContainerAllocator> *;
  using ConstRawPtr =
    const action_interfaces::msg::MagneticSpherical_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<action_interfaces::msg::MagneticSpherical_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<action_interfaces::msg::MagneticSpherical_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      action_interfaces::msg::MagneticSpherical_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::msg::MagneticSpherical_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      action_interfaces::msg::MagneticSpherical_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::msg::MagneticSpherical_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<action_interfaces::msg::MagneticSpherical_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<action_interfaces::msg::MagneticSpherical_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__action_interfaces__msg__MagneticSpherical
    std::shared_ptr<action_interfaces::msg::MagneticSpherical_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__action_interfaces__msg__MagneticSpherical
    std::shared_ptr<action_interfaces::msg::MagneticSpherical_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MagneticSpherical_ & other) const
  {
    if (this->magnetic_field_spherical != other.magnetic_field_spherical) {
      return false;
    }
    return true;
  }
  bool operator!=(const MagneticSpherical_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MagneticSpherical_

// alias to use template instance with default allocator
using MagneticSpherical =
  action_interfaces::msg::MagneticSpherical_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace action_interfaces

#endif  // ACTION_INTERFACES__MSG__DETAIL__MAGNETIC_SPHERICAL__STRUCT_HPP_
