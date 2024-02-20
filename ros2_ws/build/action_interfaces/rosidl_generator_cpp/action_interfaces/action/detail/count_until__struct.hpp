// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from action_interfaces:action/CountUntil.idl
// generated code does not contain a copyright notice

#ifndef ACTION_INTERFACES__ACTION__DETAIL__COUNT_UNTIL__STRUCT_HPP_
#define ACTION_INTERFACES__ACTION__DETAIL__COUNT_UNTIL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__action_interfaces__action__CountUntil_Goal __attribute__((deprecated))
#else
# define DEPRECATED__action_interfaces__action__CountUntil_Goal __declspec(deprecated)
#endif

namespace action_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct CountUntil_Goal_
{
  using Type = CountUntil_Goal_<ContainerAllocator>;

  explicit CountUntil_Goal_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->target_number = 0ll;
      this->period = 0.0;
    }
  }

  explicit CountUntil_Goal_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->target_number = 0ll;
      this->period = 0.0;
    }
  }

  // field types and members
  using _target_number_type =
    int64_t;
  _target_number_type target_number;
  using _period_type =
    double;
  _period_type period;

  // setters for named parameter idiom
  Type & set__target_number(
    const int64_t & _arg)
  {
    this->target_number = _arg;
    return *this;
  }
  Type & set__period(
    const double & _arg)
  {
    this->period = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    action_interfaces::action::CountUntil_Goal_<ContainerAllocator> *;
  using ConstRawPtr =
    const action_interfaces::action::CountUntil_Goal_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<action_interfaces::action::CountUntil_Goal_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<action_interfaces::action::CountUntil_Goal_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      action_interfaces::action::CountUntil_Goal_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::action::CountUntil_Goal_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      action_interfaces::action::CountUntil_Goal_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::action::CountUntil_Goal_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<action_interfaces::action::CountUntil_Goal_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<action_interfaces::action::CountUntil_Goal_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__action_interfaces__action__CountUntil_Goal
    std::shared_ptr<action_interfaces::action::CountUntil_Goal_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__action_interfaces__action__CountUntil_Goal
    std::shared_ptr<action_interfaces::action::CountUntil_Goal_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CountUntil_Goal_ & other) const
  {
    if (this->target_number != other.target_number) {
      return false;
    }
    if (this->period != other.period) {
      return false;
    }
    return true;
  }
  bool operator!=(const CountUntil_Goal_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CountUntil_Goal_

// alias to use template instance with default allocator
using CountUntil_Goal =
  action_interfaces::action::CountUntil_Goal_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace action_interfaces


#ifndef _WIN32
# define DEPRECATED__action_interfaces__action__CountUntil_Result __attribute__((deprecated))
#else
# define DEPRECATED__action_interfaces__action__CountUntil_Result __declspec(deprecated)
#endif

namespace action_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct CountUntil_Result_
{
  using Type = CountUntil_Result_<ContainerAllocator>;

  explicit CountUntil_Result_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->reached_number = 0ll;
    }
  }

  explicit CountUntil_Result_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->reached_number = 0ll;
    }
  }

  // field types and members
  using _reached_number_type =
    int64_t;
  _reached_number_type reached_number;

  // setters for named parameter idiom
  Type & set__reached_number(
    const int64_t & _arg)
  {
    this->reached_number = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    action_interfaces::action::CountUntil_Result_<ContainerAllocator> *;
  using ConstRawPtr =
    const action_interfaces::action::CountUntil_Result_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<action_interfaces::action::CountUntil_Result_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<action_interfaces::action::CountUntil_Result_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      action_interfaces::action::CountUntil_Result_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::action::CountUntil_Result_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      action_interfaces::action::CountUntil_Result_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::action::CountUntil_Result_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<action_interfaces::action::CountUntil_Result_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<action_interfaces::action::CountUntil_Result_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__action_interfaces__action__CountUntil_Result
    std::shared_ptr<action_interfaces::action::CountUntil_Result_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__action_interfaces__action__CountUntil_Result
    std::shared_ptr<action_interfaces::action::CountUntil_Result_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CountUntil_Result_ & other) const
  {
    if (this->reached_number != other.reached_number) {
      return false;
    }
    return true;
  }
  bool operator!=(const CountUntil_Result_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CountUntil_Result_

// alias to use template instance with default allocator
using CountUntil_Result =
  action_interfaces::action::CountUntil_Result_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace action_interfaces


#ifndef _WIN32
# define DEPRECATED__action_interfaces__action__CountUntil_Feedback __attribute__((deprecated))
#else
# define DEPRECATED__action_interfaces__action__CountUntil_Feedback __declspec(deprecated)
#endif

namespace action_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct CountUntil_Feedback_
{
  using Type = CountUntil_Feedback_<ContainerAllocator>;

  explicit CountUntil_Feedback_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->current_number = 0ll;
    }
  }

  explicit CountUntil_Feedback_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->current_number = 0ll;
    }
  }

  // field types and members
  using _current_number_type =
    int64_t;
  _current_number_type current_number;

  // setters for named parameter idiom
  Type & set__current_number(
    const int64_t & _arg)
  {
    this->current_number = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    action_interfaces::action::CountUntil_Feedback_<ContainerAllocator> *;
  using ConstRawPtr =
    const action_interfaces::action::CountUntil_Feedback_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<action_interfaces::action::CountUntil_Feedback_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<action_interfaces::action::CountUntil_Feedback_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      action_interfaces::action::CountUntil_Feedback_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::action::CountUntil_Feedback_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      action_interfaces::action::CountUntil_Feedback_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::action::CountUntil_Feedback_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<action_interfaces::action::CountUntil_Feedback_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<action_interfaces::action::CountUntil_Feedback_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__action_interfaces__action__CountUntil_Feedback
    std::shared_ptr<action_interfaces::action::CountUntil_Feedback_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__action_interfaces__action__CountUntil_Feedback
    std::shared_ptr<action_interfaces::action::CountUntil_Feedback_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CountUntil_Feedback_ & other) const
  {
    if (this->current_number != other.current_number) {
      return false;
    }
    return true;
  }
  bool operator!=(const CountUntil_Feedback_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CountUntil_Feedback_

// alias to use template instance with default allocator
using CountUntil_Feedback =
  action_interfaces::action::CountUntil_Feedback_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace action_interfaces


// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'goal'
#include "action_interfaces/action/detail/count_until__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__action_interfaces__action__CountUntil_SendGoal_Request __attribute__((deprecated))
#else
# define DEPRECATED__action_interfaces__action__CountUntil_SendGoal_Request __declspec(deprecated)
#endif

namespace action_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct CountUntil_SendGoal_Request_
{
  using Type = CountUntil_SendGoal_Request_<ContainerAllocator>;

  explicit CountUntil_SendGoal_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    goal(_init)
  {
    (void)_init;
  }

  explicit CountUntil_SendGoal_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    goal(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _goal_type =
    action_interfaces::action::CountUntil_Goal_<ContainerAllocator>;
  _goal_type goal;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__goal(
    const action_interfaces::action::CountUntil_Goal_<ContainerAllocator> & _arg)
  {
    this->goal = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    action_interfaces::action::CountUntil_SendGoal_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const action_interfaces::action::CountUntil_SendGoal_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<action_interfaces::action::CountUntil_SendGoal_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<action_interfaces::action::CountUntil_SendGoal_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      action_interfaces::action::CountUntil_SendGoal_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::action::CountUntil_SendGoal_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      action_interfaces::action::CountUntil_SendGoal_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::action::CountUntil_SendGoal_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<action_interfaces::action::CountUntil_SendGoal_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<action_interfaces::action::CountUntil_SendGoal_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__action_interfaces__action__CountUntil_SendGoal_Request
    std::shared_ptr<action_interfaces::action::CountUntil_SendGoal_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__action_interfaces__action__CountUntil_SendGoal_Request
    std::shared_ptr<action_interfaces::action::CountUntil_SendGoal_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CountUntil_SendGoal_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->goal != other.goal) {
      return false;
    }
    return true;
  }
  bool operator!=(const CountUntil_SendGoal_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CountUntil_SendGoal_Request_

// alias to use template instance with default allocator
using CountUntil_SendGoal_Request =
  action_interfaces::action::CountUntil_SendGoal_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace action_interfaces


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__action_interfaces__action__CountUntil_SendGoal_Response __attribute__((deprecated))
#else
# define DEPRECATED__action_interfaces__action__CountUntil_SendGoal_Response __declspec(deprecated)
#endif

namespace action_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct CountUntil_SendGoal_Response_
{
  using Type = CountUntil_SendGoal_Response_<ContainerAllocator>;

  explicit CountUntil_SendGoal_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  explicit CountUntil_SendGoal_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  // field types and members
  using _accepted_type =
    bool;
  _accepted_type accepted;
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;

  // setters for named parameter idiom
  Type & set__accepted(
    const bool & _arg)
  {
    this->accepted = _arg;
    return *this;
  }
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    action_interfaces::action::CountUntil_SendGoal_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const action_interfaces::action::CountUntil_SendGoal_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<action_interfaces::action::CountUntil_SendGoal_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<action_interfaces::action::CountUntil_SendGoal_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      action_interfaces::action::CountUntil_SendGoal_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::action::CountUntil_SendGoal_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      action_interfaces::action::CountUntil_SendGoal_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::action::CountUntil_SendGoal_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<action_interfaces::action::CountUntil_SendGoal_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<action_interfaces::action::CountUntil_SendGoal_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__action_interfaces__action__CountUntil_SendGoal_Response
    std::shared_ptr<action_interfaces::action::CountUntil_SendGoal_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__action_interfaces__action__CountUntil_SendGoal_Response
    std::shared_ptr<action_interfaces::action::CountUntil_SendGoal_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CountUntil_SendGoal_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const CountUntil_SendGoal_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CountUntil_SendGoal_Response_

// alias to use template instance with default allocator
using CountUntil_SendGoal_Response =
  action_interfaces::action::CountUntil_SendGoal_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace action_interfaces

namespace action_interfaces
{

namespace action
{

struct CountUntil_SendGoal
{
  using Request = action_interfaces::action::CountUntil_SendGoal_Request;
  using Response = action_interfaces::action::CountUntil_SendGoal_Response;
};

}  // namespace action

}  // namespace action_interfaces


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__action_interfaces__action__CountUntil_GetResult_Request __attribute__((deprecated))
#else
# define DEPRECATED__action_interfaces__action__CountUntil_GetResult_Request __declspec(deprecated)
#endif

namespace action_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct CountUntil_GetResult_Request_
{
  using Type = CountUntil_GetResult_Request_<ContainerAllocator>;

  explicit CountUntil_GetResult_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init)
  {
    (void)_init;
  }

  explicit CountUntil_GetResult_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    action_interfaces::action::CountUntil_GetResult_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const action_interfaces::action::CountUntil_GetResult_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<action_interfaces::action::CountUntil_GetResult_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<action_interfaces::action::CountUntil_GetResult_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      action_interfaces::action::CountUntil_GetResult_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::action::CountUntil_GetResult_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      action_interfaces::action::CountUntil_GetResult_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::action::CountUntil_GetResult_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<action_interfaces::action::CountUntil_GetResult_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<action_interfaces::action::CountUntil_GetResult_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__action_interfaces__action__CountUntil_GetResult_Request
    std::shared_ptr<action_interfaces::action::CountUntil_GetResult_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__action_interfaces__action__CountUntil_GetResult_Request
    std::shared_ptr<action_interfaces::action::CountUntil_GetResult_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CountUntil_GetResult_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const CountUntil_GetResult_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CountUntil_GetResult_Request_

// alias to use template instance with default allocator
using CountUntil_GetResult_Request =
  action_interfaces::action::CountUntil_GetResult_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace action_interfaces


// Include directives for member types
// Member 'result'
// already included above
// #include "action_interfaces/action/detail/count_until__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__action_interfaces__action__CountUntil_GetResult_Response __attribute__((deprecated))
#else
# define DEPRECATED__action_interfaces__action__CountUntil_GetResult_Response __declspec(deprecated)
#endif

namespace action_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct CountUntil_GetResult_Response_
{
  using Type = CountUntil_GetResult_Response_<ContainerAllocator>;

  explicit CountUntil_GetResult_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  explicit CountUntil_GetResult_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  // field types and members
  using _status_type =
    int8_t;
  _status_type status;
  using _result_type =
    action_interfaces::action::CountUntil_Result_<ContainerAllocator>;
  _result_type result;

  // setters for named parameter idiom
  Type & set__status(
    const int8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__result(
    const action_interfaces::action::CountUntil_Result_<ContainerAllocator> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    action_interfaces::action::CountUntil_GetResult_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const action_interfaces::action::CountUntil_GetResult_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<action_interfaces::action::CountUntil_GetResult_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<action_interfaces::action::CountUntil_GetResult_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      action_interfaces::action::CountUntil_GetResult_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::action::CountUntil_GetResult_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      action_interfaces::action::CountUntil_GetResult_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::action::CountUntil_GetResult_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<action_interfaces::action::CountUntil_GetResult_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<action_interfaces::action::CountUntil_GetResult_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__action_interfaces__action__CountUntil_GetResult_Response
    std::shared_ptr<action_interfaces::action::CountUntil_GetResult_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__action_interfaces__action__CountUntil_GetResult_Response
    std::shared_ptr<action_interfaces::action::CountUntil_GetResult_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CountUntil_GetResult_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const CountUntil_GetResult_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CountUntil_GetResult_Response_

// alias to use template instance with default allocator
using CountUntil_GetResult_Response =
  action_interfaces::action::CountUntil_GetResult_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace action_interfaces

namespace action_interfaces
{

namespace action
{

struct CountUntil_GetResult
{
  using Request = action_interfaces::action::CountUntil_GetResult_Request;
  using Response = action_interfaces::action::CountUntil_GetResult_Response;
};

}  // namespace action

}  // namespace action_interfaces


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'feedback'
// already included above
// #include "action_interfaces/action/detail/count_until__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__action_interfaces__action__CountUntil_FeedbackMessage __attribute__((deprecated))
#else
# define DEPRECATED__action_interfaces__action__CountUntil_FeedbackMessage __declspec(deprecated)
#endif

namespace action_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct CountUntil_FeedbackMessage_
{
  using Type = CountUntil_FeedbackMessage_<ContainerAllocator>;

  explicit CountUntil_FeedbackMessage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    feedback(_init)
  {
    (void)_init;
  }

  explicit CountUntil_FeedbackMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    feedback(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _feedback_type =
    action_interfaces::action::CountUntil_Feedback_<ContainerAllocator>;
  _feedback_type feedback;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__feedback(
    const action_interfaces::action::CountUntil_Feedback_<ContainerAllocator> & _arg)
  {
    this->feedback = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    action_interfaces::action::CountUntil_FeedbackMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const action_interfaces::action::CountUntil_FeedbackMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<action_interfaces::action::CountUntil_FeedbackMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<action_interfaces::action::CountUntil_FeedbackMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      action_interfaces::action::CountUntil_FeedbackMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::action::CountUntil_FeedbackMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      action_interfaces::action::CountUntil_FeedbackMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<action_interfaces::action::CountUntil_FeedbackMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<action_interfaces::action::CountUntil_FeedbackMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<action_interfaces::action::CountUntil_FeedbackMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__action_interfaces__action__CountUntil_FeedbackMessage
    std::shared_ptr<action_interfaces::action::CountUntil_FeedbackMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__action_interfaces__action__CountUntil_FeedbackMessage
    std::shared_ptr<action_interfaces::action::CountUntil_FeedbackMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CountUntil_FeedbackMessage_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->feedback != other.feedback) {
      return false;
    }
    return true;
  }
  bool operator!=(const CountUntil_FeedbackMessage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CountUntil_FeedbackMessage_

// alias to use template instance with default allocator
using CountUntil_FeedbackMessage =
  action_interfaces::action::CountUntil_FeedbackMessage_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace action_interfaces

#include "action_msgs/srv/cancel_goal.hpp"
#include "action_msgs/msg/goal_info.hpp"
#include "action_msgs/msg/goal_status_array.hpp"

namespace action_interfaces
{

namespace action
{

struct CountUntil
{
  /// The goal message defined in the action definition.
  using Goal = action_interfaces::action::CountUntil_Goal;
  /// The result message defined in the action definition.
  using Result = action_interfaces::action::CountUntil_Result;
  /// The feedback message defined in the action definition.
  using Feedback = action_interfaces::action::CountUntil_Feedback;

  struct Impl
  {
    /// The send_goal service using a wrapped version of the goal message as a request.
    using SendGoalService = action_interfaces::action::CountUntil_SendGoal;
    /// The get_result service using a wrapped version of the result message as a response.
    using GetResultService = action_interfaces::action::CountUntil_GetResult;
    /// The feedback message with generic fields which wraps the feedback message.
    using FeedbackMessage = action_interfaces::action::CountUntil_FeedbackMessage;

    /// The generic service to cancel a goal.
    using CancelGoalService = action_msgs::srv::CancelGoal;
    /// The generic message for the status of a goal.
    using GoalStatusMessage = action_msgs::msg::GoalStatusArray;
  };
};

typedef struct CountUntil CountUntil;

}  // namespace action

}  // namespace action_interfaces

#endif  // ACTION_INTERFACES__ACTION__DETAIL__COUNT_UNTIL__STRUCT_HPP_
