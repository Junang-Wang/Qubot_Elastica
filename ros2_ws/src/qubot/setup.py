from setuptools import find_packages, setup

package_name = 'qubot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='qubot',
    maintainer_email='wangjunang94@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "cmd_mag_publisher = qubot.cmd_mag_publisher:main",
            "cmd_mag_subscriber = qubot.cmd_mag_subscriber:main",
            "sofa_sim = qubot.sofa_sim:main"
        ],
    },
)
