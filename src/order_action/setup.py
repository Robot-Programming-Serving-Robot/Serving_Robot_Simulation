from setuptools import setup

package_name = 'order_action'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hwlee20',
    maintainer_email='hwlee0108@naver.com',
    description='Action server and client for ordering drinks',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'order_action_server = order_action.order_action_server:main',
            'order_action_client = order_action.order_action_client:main',
        ],
    },
)
