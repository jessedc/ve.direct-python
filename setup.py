from setuptools import find_packages, setup

setup(
    name="ve.direct-python",
    version="0.0.1",
    description="A parser for the ve.direct protocol",
    author="Jesse Collis",
    author_email="jesse@jcmultimedia.com.au",
    url="https://github.com/jessedc/ve.direct-to-mqtt",
    packages=find_packages(exclude=["*.tests"]),
    test_suite="vedirect.tests",
    install_requires=[
        "influxdb>=5.2"
    ],
    setup_requires=[
    ],
    tests_require=[
    ],
    entry_points={
        "console_scripts": [
            "vedirect = vedirect.__main__:main",
        ],
    },
)
