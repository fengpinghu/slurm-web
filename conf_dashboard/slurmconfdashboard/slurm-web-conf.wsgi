import logging, sys
logging.basicConfig(stream=sys.stderr)
from slurmconfdashboard.slurmwebconf import app as application
