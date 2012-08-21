from sqlalchemy import *
import datetime

class FileIndex:
    __db=None
    __db_name=None
    __metadata=None
    __file_index=None
    def __init__(self):
        self.__db= create_engine('sqlite:///.db/info.db')
        self.__db.echo = False 
        self.__metadata= MetaData(self.__db)
        #trans = self.db.begin()

        #for name, table in self.metadata.tables.items():
            #print table.delete()
            #self.db.execute(table.delete())
        self.InitIndex()
        #trans.commit()
    def InitIndex(self):
        self.__file_index = Table('index', self.__metadata,
            Column('file_id', Integer, primary_key=True),
            Column('filename', String),
            Column('hash', String),
            Column('rows', Integer),
            Column('size', Integer), 
            Column('time',  DateTime(timezone=True), default=datetime.datetime.utcnow)
        )
        self.__file_index.create()
        #see code here http://stackoverflow.com/questions/414952/sqlalchemy-datetime-timezone
    def addEntry(self, entry):
        """ Should add something like this {'filename': 'main.c', 'hash': 'aabbcc','rows':123,'size':2343} """
        operation = self.__file_index.insert()
        result=operation.execute(entry)
        print result
        
    def getAll(self):
        operation = self.__file_index.select()
        result = operation.execute()
        row = result.fetchone()
        for row in result:
            print row.filename, 'is', row.size, ' bytes'
            
    def now():
        return datetime.datetime.now()
if __name__ == "__main__":
    indexer=FileIndex()
    indexer.addEntry({'filename': 'main.c', 'hash': 'aabbcc','rows':123,'size':2343})
    indexer.getAll()
