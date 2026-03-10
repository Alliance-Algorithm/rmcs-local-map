#pragma once

#include "util/parameter.hpp"

#include <rclcpp/node.hpp>
#include <stdexcept>

namespace param {
inline auto node = static_cast<rclcpp::Node*>(nullptr);

inline auto bind(rclcpp::Node& owner) -> void { node = &owner; }

template <typename T>
inline auto get(const std::string& name) {
    if (node == nullptr)
        throw std::runtime_error("param::bind(node) must be called before param::get");

    auto param = T{};
    node->get_parameter<T>(name, param);
    return param;
}

} // namespace param
