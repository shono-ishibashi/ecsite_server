from sqlalchemy import create_engine, MetaData
from pprint import pprint


engine = create_engine(
    'mysql+pymysql://ecsite:ecsite_password@db:3306/ecsite_database')

metadata =MetaData()

metadata.reflect(engine)
pprint(vars(metadata))
