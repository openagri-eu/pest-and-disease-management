# Import all the models, so that Base has them before being
# imported by Alembic

from models import *
from base_class import Base