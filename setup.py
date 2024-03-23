import os
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension, CppExtension
from distutils.sysconfig import get_config_vars

(opt,) = get_config_vars("OPT")
os.environ["OPT"] = " ".join(
    flag for flag in opt.split() if flag != "-Wstrict-prototypes"
)

src = "src"
sources = [
    os.path.join(root, file)
    for root, dirs, files in os.walk(src)
    for file in files
    if file.endswith(".cpp") or file.endswith(".cu")
]

# def get_python_paths():
#     from distutils.sysconfig import get_python_inc, get_config_var
#     return {
#         'include_dirs': [get_python_inc()],
#         'library_dirs': [get_config_var('LIBDIR')],
#     }
# python_paths = get_python_paths()



setup(
    name="scannet_segmentator",
    version="1.0",
    install_requires=["torch", "numpy", "numba"],
    packages=["scannet_segmentator"],
    package_dir={"scannet_segmentator": "functions"},
    ext_modules=[
        CppExtension(
            name='libsegmentator._C',
            sources=sources,
            extra_compile_args=['-std=c++14'],
        )
    ],
    # include_dirs=[*python_paths['include_dirs']],
    cmdclass={"build_ext": BuildExtension},
)

# include_dirs 什么时候需要加?