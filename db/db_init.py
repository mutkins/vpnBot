from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


# Declarative method
engine = create_engine("sqlite:////etc/ducky_vpn_data/ducky_vpn.db", echo=True)
Base = declarative_base()


