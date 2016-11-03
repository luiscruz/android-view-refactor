from setuptools import setup

setup(
    name='android-view-refactor',
    version='0.1',
    py_modules=['android_view_refactor'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        android-view-refactor=android_view_refactor:tool
    ''',
)
