cmake_minimum_required(VERSION 3.10)

project(simulation LANGUAGES CXX CUDA)

# Set the CUDA toolkit root directory
set(CUDAToolkit_ROOT "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.5")

# Find CUDA and pybind11 packages
find_package(CUDAToolkit REQUIRED)
find_package(PythonLibs REQUIRED)
find_package(pybind11 REQUIRED)

include_directories(${CUDAToolkit_INCLUDE_DIRS})
include_directories(${PYTHON_INCLUDE_DIRS})
include_directories(${PYBIND11_INCLUDE_DIRS})

# Add CUDA source files
add_library(simulation MODULE
    parameters.cu
    simulation_wrapper.cpp
)

set_target_properties(simulation PROPERTIES
    PREFIX "${PYTHON_MODULE_PREFIX}"
    SUFFIX "${PYTHON_MODULE_EXTENSION}"
)

target_link_libraries(simulation PRIVATE ${CUDAToolkit_LIBRARIES} pybind11::module)
