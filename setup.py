#!/usr/bin/env python3
#!/usr/bin/env python这种用法是为了防止操作系统用户没有将python装在默认的/usr/bin路径里。
#当系统看到这一行的时候，首先会到env设置里查找python的安装路径，再调用对应路径下的解释器程序完成操作。
#比
# -*- coding: utf-8 -*-  识别中文编码
# © 2015 James R. Barlow: github.com/jbarlow83
#
# This file is part of OCRmyPDF.
#
# OCRmyPDF is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OCRmyPDF is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OCRmyPDF.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function, unicode_literals
#Python提供了__future__模块，把下一个新版本的特性导入到当前版本
#可以在当前版本中测试一些新版本的特性
#在2.7版本的代码中，可以通过unicode_literals来使用Python 3.x的新的语法


import sys

if sys.version_info < (3, 6):
    print("Python 3.6 or newer is required", file=sys.stderr)
    sys.exit(1)

from setuptools import setup, find_packages   #setuptools 安装工具模块
from subprocess import STDOUT, check_output, CalledProcessError   #subprocess fork一个子进程，并让这个子进程exec另外一个程序相关模块
from collections.abc import Mapping   #collections模块提供了一些有用的集合类
import re    #re模块提供正则表达式操作

# pylint: disable=w0613


command = next((arg for arg in sys.argv[1:] if not arg.startswith('-')), '')   #获得shell命令的输出，调用Linuxshell得到命令结果
if command.startswith('install') or command in [
    'check',
    'test',
    'nosetests',
    'easy_install',
]:
    forced = '--force' in sys.argv
    if forced:
        print("The argument --force is deprecated. Please discontinue use.")


if 'upload' in sys.argv[1:]:
    print('Use twine to upload the package - setup.py upload is insecure')
    sys.exit(1)

tests_require = open('requirements/test.txt', encoding='utf-8').read().splitlines()


def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='ocrmypdf',
    description='OCRmyPDF adds an OCR text layer to scanned PDF files, allowing them to be searched',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/jbarlow83/OCRmyPDF',
    author='James R. Barlow',
    author_email='jim@purplerock.ca',
    packages=find_packages('src', exclude=["tests", "tests.*"]),
    package_dir={'': 'src'},
    keywords=['PDF', 'OCR', 'optical character recognition', 'PDF/A', 'scanning'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=' >= 3.6',
    setup_requires=[  # can be removed whenever we can drop pip 9 support
        'cffi >= 1.9.1',  # to build the leptonica module
        'pytest-runner',  # to enable python setup.py test
        'setuptools_scm',  # so that version will work
        'setuptools_scm_git_archive',  # enable version from github tarballs
    ],
    use_scm_version={'version_scheme': 'post-release'},
    cffi_modules=['src/ocrmypdf/lib/compile_leptonica.py:ffibuilder'],
    install_requires=[
        'chardet >= 3.0.4, < 4',  # unlisted requirement of pdfminer.six 20181108
        'cffi >= 1.9.1',  # must be a setup and install requirement
        'img2pdf >= 0.3.0, < 0.4',  # pure Python, so track HEAD closely
        'pdfminer.six == 20181108 ; sys_platform != "darwin"',
        'pikepdf >= 1.1.0, < 2',
        'Pillow >= 4.0.0, != 5.1.0 ; sys_platform == "darwin"',
        # Pillow < 4 has BytesIO/TIFF bug w/img2pdf 0.2.3
        # block 5.1.0, broken wheels
        'reportlab >= 3.3.0',  # oldest released version with sane image handling
        'ruffus >= 2.7.0',
    ],
    extras_require={'pdfminer': ['pdfminer.six == 20181108']},
    tests_require=tests_require,
    entry_points={'console_scripts': ['ocrmypdf = ocrmypdf.__main__:run_pipeline']},
    package_data={'ocrmypdf': ['data/sRGB.icc']},
    include_package_data=True,
    zip_safe=False,
    project_urls={
        'Documentation': 'https://ocrmypdf.readthedocs.io/',
        'Source': 'https://github.com/jbarlow83/ocrmypdf',
        'Tracker': 'https://github.com/jbarlow83/ocrmypdf/issues',
    },
)
