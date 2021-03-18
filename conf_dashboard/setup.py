from setuptools import setup

setup(
    name='slurm-web-dashboard-backend',
    packages=['slurmconfdashboard'],
    version='3.9.6',
    long_description=__doc__,
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)

