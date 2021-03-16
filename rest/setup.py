from setuptools import setup

setup(
    name='slurm-web-restapi',
    packages=['slurmrestapi'],
    version='3.9.6',
    long_description=__doc__,
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'pyslurm', 'clustershell', 'python-ldap', 'itsdangerous', 'redis']
)
