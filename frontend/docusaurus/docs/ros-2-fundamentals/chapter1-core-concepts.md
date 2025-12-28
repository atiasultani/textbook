---
sidebar_position: 3
title: 'Chapter 1: Core ROS 2 Concepts'
---

# Chapter 1: Core ROS 2 Concepts

## Learning Objectives

After completing this chapter, students will be able to:
- Explain the basic ROS 2 architecture and its key components
- Create and run simple publisher and subscriber nodes
- Understand the difference between topics, services, and actions
- Implement basic communication patterns in ROS 2

## Introduction

ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It is a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms.

In this chapter, we'll explore the fundamental concepts that form the backbone of ROS 2, including nodes, topics, services, and actions.

## ROS 2 Nodes

[Content about ROS 2 nodes with explanations and diagrams]

### Code Examples

```python
# Example: Simple publisher node
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

```cpp
// Example: Simple publisher node in C++
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class MinimalPublisher : public rclcpp::Node
{
public:
    MinimalPublisher()
    : Node("minimal_publisher"), count_(0)
    {
        publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
        timer_ = this->create_wall_timer(
            500ms, std::bind(&MinimalPublisher::timer_callback, this));
    }

private:
    void timer_callback()
    {
        auto message = std_msgs::msg::String();
        message.data = "Hello, world! " + std::to_string(count_++);
        RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
        publisher_->publish(message);
    }
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    size_t count_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MinimalPublisher>());
    rclcpp::shutdown();
    return 0;
}
```

## ROS 2 Topics and Message Passing

[Content about topics with pub/sub patterns]

## ROS 2 Services

[Content about services with request/response patterns]

## ROS 2 Actions

[Content about actions with goal/result/feedback patterns]

## ROS 2 Architecture Diagrams

![ROS 2 Architecture](/img/ros2-fundamentals/ros2-architecture.svg)

*Figure 1: ROS 2 Architecture showing nodes, topics, services, and actions*

![Node Communication Patterns](/img/ros2-fundamentals/node-communication.svg)

*Figure 2: Different communication patterns in ROS 2: topics (pub/sub), services (req/rep), and actions (goal/feedback/result)*

## Exercises

### Hands-on Exercise 1: Creating Publisher and Subscriber Nodes

**Objective**: Create and run a publisher node and a subscriber node that communicate over a topic.

**Requirements**:
- ROS 2 installation (Humble Hawksbill or later)
- Basic Python or C++ knowledge

**Steps**:
1. Create a new ROS 2 package for the exercise
2. Implement the publisher node code shown above
3. Create a subscriber node that listens to the same topic
4. Build and run both nodes
5. Observe the message exchange

**Expected Outcome**: The publisher should send messages at regular intervals and the subscriber should receive and print them.

## Assessment Questions

### Question 1
**Question**: What is a ROS 2 node?

**Answer**: A node is an executable that uses ROS 2 to communicate with other nodes. Nodes are the fundamental building blocks of a ROS 2 system.

### Question 2
**Question**: What is the difference between topics and services in ROS 2?

**Answer**: Topics provide asynchronous, many-to-many communication using a publish/subscribe model, while services provide synchronous, one-to-one communication using a request/response model.

## Physical Activities

### Activity 1: Human Pub/Sub System

**Objective**: Demonstrate the publish/subscribe communication pattern using humans as nodes.

**Materials Needed**:
- Index cards
- A large room

**Steps**:
1. Divide students into "publisher" and "subscriber" groups
2. Publishers write messages on index cards and place them in a shared location
3. Subscribers periodically check the shared location and read the messages
4. Discuss how this models the pub/sub pattern in ROS 2

**Learning Outcome**: Students understand the asynchronous nature of topic-based communication.

## Summary

In this chapter, we covered the core concepts of ROS 2 including nodes, topics, services, and actions. These fundamental building blocks form the basis for all ROS 2 applications.

## Key Takeaways

- Nodes are the basic execution units in ROS 2
- Topics enable asynchronous communication through publish/subscribe
- Services enable synchronous communication through request/response
- Actions provide goal-oriented communication with feedback
- These concepts work together to create distributed robotic systems

## References and Additional Resources

- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [ROS 2 Design](https://design.ros2.org/)