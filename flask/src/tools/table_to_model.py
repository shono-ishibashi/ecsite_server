from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.inspection import inspect


Base = automap_base()


engine = create_engine(
    'mysql+pymysql://ecsite:ecsite_password@db:3306/ecsite_database')
Base.prepare(engine, reflect=True)

# 生成されたmodel

# modelが持つfield(property)を利用するためにinspectionの機能を使っている
mapper = inspect(Base.classes.users)
for prop in mapper.iterate_properties:
    print("\t", prop.key, type(prop))
