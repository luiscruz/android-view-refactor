from setuptools import setup, find_packages

setup(
    name='android-view-refactor',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'lxml',
    ],
    entry_points='''
        [console_scripts]
        android-view-refactor=android_view_refactor.android_view_refactor:tool
    ''',
)
