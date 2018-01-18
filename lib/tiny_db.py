'''
This is tiny key-value database
GrayLoo @ 20180117
'''
import cPickle as pickle

slots = ['TinyDb']

class TinyDb(object):
    def __init__(self, dest):
        self.dest = dest
        self.tables = {}
        self.table_info = {}
        self.table_info, self.tables = self.__load_db()
        print("Initialized database")

    def add_table(self, table_name, keys, primary_key=None):
        if table_name not in self.table_info:
            if not primary_key:
                primary_key = keys[0]
            self.table_info[table_name] = (primary_key, keys)
            print("table [%s] added" %table_name)
            return 0
        else:
            print("table [%s] already exists, doing nothing" %table_name)
            return 1

    def drop_table(self, table_name):
        if table_name in self.table_info:
            del self.table_info[table_name]
            if table_name in self.tables:
                del self.tables[table_name]
            print("table [%s] dropped" %table_name)
            return 0
        else:
            print("table [%s] not exist, doing nothing" %table_name)
            return 1

    def insert_record(self, table_name, key_values):
        if table_name not in self.table_info:
            print("table [%s] not exist, insert record failed" %table_name)
            return 1
        if table_name not in self.tables:
            self.tables[table_name] = {}
        primary_key = self.table_info[table_name][0]
        if primary_key not in key_values:
            print("primary key [%s] not found in args, insert record failed" %primary_key)
            return 1
        primary_value = key_values[primary_key]
        self.tables[table_name][primary_value] = key_values
        print("record added to table [%s]" %table_name)
        return 0
    
    def delete_record(self, table_name, primary_key):
        if table_name not in self.tables:
            print("table [%s] not exist, doing nothing" %table_name)
            return 1
        table = self.tables[table_name]
        if primary_key not in table:
            print("record [%s] not exist in table [%s]" %(primary_key, table_name))
            return 1
        del table[primary_key]
        return 0
    
    def find(self, table_name, primary_value=None):
        if table_name not in self.tables:
            print("table [%s] not exist" %table_name)
            return []
        table = self.tables[table_name]
        if not primary_value:
            return table
        else:
            if primary_value not in table:
                return []
            else:
                return table[primary_value]
    
    def find_all(self, table_name):
        return self.find(table_name)
        
    def get_table_info(self, table_name):
        if table_name not in self.table_info:
            return ''
        else:
            return self.table_info[table_name]
    
    def __load_db(self):
        table_info_file = self.dest + "table_info.db"
        tables_file = self.dest + "tables.db"
        try:
            with open(table_info_file, "rb") as f:
                table_info = pickle.load(f)
            with open(tables_file, "rb") as f:
                tables = pickle.load(f)
            print("database loaded")
            return table_info, tables
        except Exception as e:
            print("load database file failed, will initialize database as empty")
            return {}, {}

    def dump(self):
        table_info_file = self.dest + "table_info.db"
        tables_file = self.dest + "tables.db"
        with open(table_info_file, "wb") as f:
            pickle.dump(self.table_info, f)
        with open(tables_file, "wb") as f:
            pickle.dump(self.tables, f)
        print("database dumped")

    def __del__(self):
        self.dump()


if __name__ == "__main__":
    '''
    example and unit test goes here
    '''
    # before use tiny db, we should make a TinyDb instance
    db = TinyDb("../data/")

    ############################### add table #################################
    # add a table called "user" to database, which has 3 properties(name, age, email), and use "name" as primary key
    db.add_table("user", ["name", "age", "email"])
    # add another table
    db.add_table("another_table", ["a", "b", "c"])

    ############################## drop table #################################
    # drop a table will delete all the records in this table
    db.drop_table("another_table")
    
    ############################# add records #################################
    # add a record to table "user", whose data is {"name": "spoon", "age": 27, "email": "spoon@touchfishtech.com"}
    db.insert_record("user", {"name": "spoon", "age": 27, "email": "spoon@touchfishtech.com"})
    # add another record
    db.insert_record("user", {"name": "grayloo", "age": 27, "email": "grayloo@touchfishtech.com"})

    ############################# query a record in a specified table ###########################
    # query a record in table "user", whose primary key's value is "spoon"(aka name = "spoon")
    result = db.find("user", "spoon")
    print(result)
    # get all records in this table
    all_records = db.find_all("user")
    print(all_records)

    ############################# query table information #######################################
    # query table information by table's name, in case we forget the properties of a table
    table_info = db.get_table_info("user")
    # the first element in the result is the primary key
    print(table_info)

    ############################ dump database to file ##########################################
    # we can dump the database manually, or just let the TinyDb's destructor function(aka __del__) do the dump work automatically
    db.dump()