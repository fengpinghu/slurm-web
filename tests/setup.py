from setuptools import setup

setup(
    name='slurm-web-tests',
    packages=['slurmwebtests'],
    version='3.9.6',
    long_description=__doc__,
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'mock', 'racks', 'requests', 'slurm-web-restapi', 'slurm-web-dashboard-backend']
)

