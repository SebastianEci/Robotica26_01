from setuptools import setup
import os
from glob import glob

package_name = 'dif_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name,
            ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
        (os.path.join('share', package_name, 'urdf'),
            glob('urdf/*')),
        (os.path.join('share', package_name, 'worlds'),
            glob('worlds/*')),
        (os.path.join('share', package_name, 'config'),
            glob('config/*')),
        (os.path.join('share', package_name, 'maps'),
            glob('maps/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='david',
    maintainer_email='dsantiagocardenas96@gmail.com',
    description='Robot diferencial con SLAM, AMCL, Nav2 y misiones autónomas',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'odom_tf = dif_bot.odom_tf:main',
            'mission_commander = dif_bot.mission_commander:main',
        ],
    },
)
