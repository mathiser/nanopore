import os

from backend import file_types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db_declarative import Fast5, Read, Base


class DB:
    Base = Base
    def __init__(self):
        self.engine = create_engine('sqlite:///%s' % open("database/sql_path.txt", 'r').readline())
        if not os.path.isfile(open("database/sql_path.txt", 'r').readline()):
            self.Base.metadata.create_all(self.engine)
            print("New DB created")

        self.DBSession = sessionmaker(bind=self.engine)

    def insert_fast5(self, fast5: file_types.Fast5):
        session = self.DBSession()
        session.add(Fast5(filepath=fast5.filepath, filename=fast5.filename))
        session.commit()
        session.close()

    def insert_read(self, read: file_types.Read):
        session = self.DBSession()
        session.add(Read(filepath=read.filepath, filename=read.filename))
        session.commit()
        session.close()

    def get_fast5(self, filename):
        session = self.DBSession()
        f5 = session.query(Fast5).filter(Fast5.filename == filename).first()
        session.close()
        return f5



