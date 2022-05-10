from setuptools import setup

setup(
    name='custom_serialize',
    packages=[
        'custom_serialize',
        'custom_serialize/serializer',
        'custom_serialize/serializer/json',
        'custom_serialize/serializer/toml',
        'custom_serialize/serializer/yaml',
    ],
    version='1.0.0',
    author='vestriger',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.3'],
    test_suite='tests',
    scripts=['custom_serialize/serializer_cmd.py']
)