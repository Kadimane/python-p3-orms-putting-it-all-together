import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS dogs (
        id INTEGER PRIMARY KEY,
        name TEXT,
        breed TEXT
        )
        """    

        CURSOR.execute(sql)

    @classmethod
    def drop_table(self):
        sql = """
        DROP TABLE IF EXISTS dogs
        """  

        CURSOR.execute(sql)  
        CONN.commit()

    def save(self):
        if self.id is None:
            sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.breed))
            self.id = CURSOR.lastrowid
            CONN.commit()
        else:
            sql = """
            UPDATE dogs SET name=?, breed=? WHERE id=?
            """
            CURSOR.execute(sql, (self.name, self.breed, self.id))
            CONN.commit()

        return self

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog   
    
    @classmethod
    def new_from_db(cls, data):
        id, name, breed = data
        dog = cls(name, breed)
        dog.id = id
        return dog
    
    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM dogs"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        dogs = []
        for row in rows:
            dog = cls.new_from_db(row)
            dogs.append(dog)
        return dogs
    
    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM dogs WHERE name = ?"
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        if row is not None:
            dog = cls.new_from_db(row)
            return dog
        else:
            return None
        
    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM dogs WHERE id = ?"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row is not None:
            dog = cls.new_from_db(row)
            return dog
        else:
            return None    
        
    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name(name)
        if dog is not None and dog.breed == breed:
            return dog
        else:
            return cls.create(name, breed)    
        
    def update(self):
        sql = "UPDATE dogs SET name = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()
