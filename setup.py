# -*- coding: UTF-8 -*-
"""
Setup

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
import os, shutil
from cx_Freeze import setup, Executable
import app
from app.core.util import *

# constants
application_title = app.APPLICATION_NAME
main_python_file = "app.py"
version = app.__version__
includes = ["atexit"]
excludes = ["nt",
            'pdb',
            '_ssl',
            "Pyrex",
            "ntpath",
            'doctest',
            "tkinter",
            'pyreadline',
            "matplotlib",
            "scipy.linalg",
            "scipy.special",
            "numpy.core._dotblas"]

included_files = [('LICENSE', 'LICENSE')]

# add platform-specific files
if OS_WIN:
    included_files.append(('resources/bdist/libEGL.dll', 'libEGL.dll'))

# try to build the resource file
try:
    print("Building resource file")
    os.system("pyside6-rcc -o app/resources.py resources/resources.qrc")
except:
    print("Failed to build resource file")

if app.DEBUG:
    print("WARNING!")
    print("DEBUG mode is ON")

setup(
    name=application_title,
    version=version,
    url=app.APPLICATION_WEB,

    author=app.APPLICATION_AUTHOR,
    author_email=app.APPLICATION_EMAIL,
    description=app.DESCRIPTION,
    long_description=app.DESCRIPTION_LONG,
    keywords=app.KEYWORDS,
    license=app.LICENSE,

    requires=['cx_Freeze', 'PySide6'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Desktop Environment :: Gnome',
        'Topic :: Desktop Environment :: K Desktop Environment (KDE)'
    ],

    options={
        "build_exe": {
            "includes": includes,
            "include_files": included_files,
            # TODO: test msvcr dll
            # "include_msvcr": True,
            "excludes": excludes,
            "silent": True
        },
        "bdist_msi": {
            "upgrade_code": app.GUID
        },
        "bdist_mac": {
            "bundle_name": f"{application_title}-{version}",
            "custom_info_plist": "resources/bdist/Info.plist",
            "iconfile": "resources/icon/icon.icns"
        },
        "bdist_dmg": {
            "volume_label": f"{application_title}-{version}"
        }
    },
    executables=[Executable(main_python_file,
                            base="Win32GUI" if sys.platform == "win32" else None,
                            icon="resources/icon/icon.ico",
                            shortcut_name=application_title,
                            shortcut_dir="ProgramMenuFolder"
                            )])

# fix Mac OS app file
if OS_MAC:
    app_contents = f"build/{application_title}-{version}.app/Contents"
    app_resources = f"{app_contents}/Resources"

    if os.path.exists(app_resources):
        shutil.copyfile("resources/bdist/qt.conf", f"{app_resources}/qt.conf")
