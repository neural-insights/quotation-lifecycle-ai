#RUN IT ONCE

from utils.db import Base, engine
import utils.models

# Create all tables in the database
Base.metadata.create_all(bind=engine)
