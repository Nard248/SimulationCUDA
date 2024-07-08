cmake_minimum_required(VERSION 3.10)

project(simulation LANGUAGES CXX CUDA)

# Set the CUDA toolkit root directory
set(CUDAToolkit_ROOT "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.5")

# Find CUDA and pybind11 packages
find_package(CUDAToolkit REQUIRED)
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 REQUIRED)

include_directories(${CUDAToolkit_INCLUDE_DIRS})
include_directories(${Python3_INCLUDE_DIRS})
include_directories(${pybind11_INCLUDE_DIRS})

# Add the Python include directory
include_directories(${Python3_INCLUDE_DIRS})

# Add the Python library directory
link_directories(${Python3_LIBRARY_DIRS})

# Add CUDA source files
add_library(simulation MODULE
    main.cu
    parameters.cu
)

set_target_properties(simulation PROPERTIES
    PREFIX "${PYTHON_MODULE_PREFIX}"
    SUFFIX "${PYTHON_MODULE_EXTENSION}"
)

target_link_libraries(simulation PRIVATE ${CUDAToolkit_LIBRARIES} ${CUDA_cufft_LIBRARY} pybind11::module Python3::Python)
