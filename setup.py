from __future__ import absolute_import

from glob import glob
import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='sm-tf-horovod-container',
    version='1.0',
    description='Library to run training with TensorFlow and Horovod on Amazon SageMaker.',
    packages=find_packages(where='src'),
    package_dir={'sm_tf_horovod_container': 'src/sm_tf_horovod_container'},
    py_modules=[os.splitext(os.basename(path))[0] for path in glob('src/*.py')],
    long_description=read('README.rst'),
    author='Indu Bharathi',
    license='Apache License 2.0',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=['sagemaker-containers==2.0.2', 'retrying==1.3.3',
                      'numpy >= 1.14'],

    dependency_links=['pip install git+https://github.com/aws/sagemaker-python-sdk-staging'],
    )

