from backend.database.database import Base, engine

from backend.database.models.company import Company
from backend.database.models.user import User
from backend.database.models.machine import Machine


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Database recreated successfully.")
