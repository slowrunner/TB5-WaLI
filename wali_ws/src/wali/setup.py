from setuptools import setup
import os
from glob import glob

package_name = 'wali'

setup(
    name=package_name,
    version='0.0.2',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('lib/' + package_name, [package_name+'/ir_dist.py']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='slowrunner',
    maintainer_email='slowrunner@users.noreply.github.com',
    description='WaLI: Wall follower Looking for Intelligence',
    license='If it works for you, let me know',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'wali_node = wali.wali_node:main',
            'test_wali_node = wali.test_wali_node:main',
            'vel_pwr_test = wali.vel_pwr_test:main',
            'battery_sub = wali.battery_sub:main',
            'ir2scan = wali.ir2scan:main',
            'ir2scan1 = wali.ir2scan1:main',
            'odometer = wali.odometer:main',
            'say_node = wali.say_node:main',
            'wander = wali.wander:main',
            'wallfollower = wali.wallfollower:main',
            'sub_tf = wali.sub_tf:main',
            'c3interface = wali.c3interface:main',
            'lifelognode = wali.lifelognode:main',
            'monitor = wali.monitor_node:main',
            'sub_ir = wali.sub_ir:main',
            'set_pose_docked = wali.set_initial_pose_docked:main',
            'set_pose_undocked = wali.set_initial_pose_undocked:main',
            'nav_to_couch_view = wali.nav_to_couch_view:main',
            'nav_to_dining = wali.nav_to_dining:main',
            'nav_to_hall_view = wali.nav_to_hall_view:main',
            'nav_to_kitchen = wali.nav_to_kitchen:main',
            'nav_to_laundry = wali.nav_to_laundry:main',
            'nav_to_office = wali.nav_to_office:main',
            'nav_to_patio_view = wali.nav_to_patio_view:main',
            'nav_to_ready = wali.nav_to_ready:main',
            'nav_to_see_front_door = wali.nav_to_see_front_door:main',
            'nav_to_table = wali.nav_to_table:main',
            'nav_to_undocked = wali.nav_to_undocked:main',
            'wali_tour = wali.wali_tour:main',
            'tour_metrics = wali.tour_metrics_node:main',
        ],
    },
)
