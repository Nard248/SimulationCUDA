from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np
import os
import sys
from distutils.command.build_ext import build_ext
from distutils.sysconfig import get_python_inc
import subprocess


# Set the correct default path for Windows
def locate_cuda():
    """Locate the CUDA environment on the system."""
    if os.name == 'nt':  # Windows
        CUDA_PATH = os.environ.get('CUDA_PATH', 'C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.4')
    else:  # Linux or MacOS
        CUDA_PATH = os.environ.get('CUDA_PATH', '/usr/local/cuda')

    # Locate nvcc binary inside the CUDA_PATH
    nvcc = os.path.join(CUDA_PATH, 'bin', 'nvcc.exe')
    if not os.path.exists(nvcc):
        raise EnvironmentError(f"The nvcc binary could not be located at: {nvcc}")

    cudaconfig = {
        'home': CUDA_PATH,
        'nvcc': nvcc,
        'include': os.path.join(CUDA_PATH, 'include'),
        'lib64': os.path.join(CUDA_PATH, 'lib', 'x64')  # Adjusted for Windows 'lib/x64'
    }

    for k, v in cudaconfig.items():
        if not os.path.exists(v):
            raise EnvironmentError(f"Could not locate the CUDA {k} path: {v}")

    return cudaconfig


CUDA = locate_cuda()


def compile_cuda_for_extension(extension):
    """Compile CUDA .cu files with nvcc for a given extension."""
    for source in extension.sources:
        if source.endswith('.cu'):
            output_file = source.replace('.cu', '.obj')
            nvcc_cmd = [
                f'"{CUDA["nvcc"]}"',
                '-c',
                f'"{source}"',
                '-o', f'"{output_file}"',
                '--compiler-options', '/MD',
                '-I', f'"{CUDA["include"]}"',
            ]
            print(f"Compiling {source} with nvcc...")
            subprocess.check_call(nvcc_cmd, shell=True)
    # Remove .cu files from sources so they don't get passed to MSVC
    extension.sources = [s for s in extension.sources if not s.endswith('.cu')]


class custom_build_ext(build_ext):
    """Custom build_ext to handle .cu files with nvcc."""

    def build_extensions(self):
        for ext in self.extensions:
            compile_cuda_for_extension(ext)
        build_ext.build_extensions(self)


extensions = [
    Extension(
        name="wrapper",
        sources=["src/wrapper.pyx", "src/parameters.cu", "src/main.cu"],  # Include .cu sources
        library_dirs=[CUDA['lib64']],
        libraries=['cudart', 'cufft'],
        language="c++",
        extra_compile_args={'msvc': ['/EHsc'], 'nvcc': ['-O3']},  # Adjust MSVC flags here
        include_dirs=[np.get_include(), CUDA['include'], get_python_inc()],
        extra_link_args=['-lcufft', '-lcudart'],
    )
]

setup(
    name="cuda_wrapper",
    ext_modules=cythonize(extensions),
    cmdclass={'build_ext': custom_build_ext},
)
