import sqlite3
import pathlib
import os
import datetime


class Model:
    '''model for note app'''


    def __init__(self):
        
        self.connection = sqlite3.connect('note.sqlite')
        print('database connected!')
        self.cursor = self.connection.cursor()
        self.db_note_table_create() # create table in database if not existed


    def db_note_table_create(self) -> None:
        '''
        Create notes table in database if not exist,
        '''
        try:
            self.cursor.execute("""CREATE TABLE notes(
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                creation_time TEXT, 
                                last_update_time TEXT,
                                title TEXT, 
                                content TEXT)""")
            print('table created')
        except sqlite3.OperationalError as e:
            print('error: ', e) 


    def db_note_get_all(self) -> list[tuple]:
        '''
        # get all notes from database, and return them as a dict

        [
            (
                1,
                "2023/09/12 12:00:00", # creation_time
                "2023/09/12 12:00:00", # last_update_time
                "some note", # title
                "note content, hello world", # content
            ),
            (
                2,
                "2023/09/12 12:00:00",
                "2023/09/12 12:00:00",
                "some note",
                "note content, hello world",
            )
        ]        
        '''
        results = self.cursor.execute("SELECT * FROM notes").fetchall()
        return results


    def db_note_get_by_id(self, id: int) -> tuple:
        '''
        # Provide id of a note, and return the found row in database as a tuple 

            (
                1, # id
                "2023/09/12 12:00:00", # creation_time
                "2023/09/12 12:00:00", # last_update_time
                "some note", # title
                "note content, hello world", # content
                )
        '''
        sql_query = f"SELECT * FROM notes WHERE id={id}"
        print(sql_query)
        result = self.cursor.execute(sql_query).fetchone()
        return result


    def db_note_create(self, title: str, content: str) -> None:
        '''
        Write new note note in database.
        '''
        sql_query = f"""
            INSERT INTO notes(creation_time, last_update_time, title, content)
                        VALUES('{self.current_time()}',
                                '{self.current_time()}',
                                '{title}',
                                '{content}')
        """
        self.cursor.execute(sql_query)
        self.connection.commit()
        print(f"new note created (title: {title}, content: {content[:20]}...) ")

    def db_note_update(self, id: int, title: str, content: str) -> None:
        '''
        Update existing note in database.
        '''
        sql_query = f"""
            UPDATE notes
            SET 
                last_update_time = '{self.current_time()}',
                title = '{title}',
                content = '{content}'
            WHERE id = {id}
        """
        self.cursor.execute(sql_query)
        self.connection.commit()
        print(f"existing note updated (id: {id},title: {title}, content: {content[:20]}...)")


    def db_note_delete(self, id_list: list[int]) -> None:
        '''
        delete or bulk delete note from database providing single id or list of id.
        '''
        for id in id_list:
            sql_query = f"""DELETE FROM notes WHERE id={id}"""
            self.cursor.execute(sql_query)
            self.connection.commit()
            print(f"Note {id} deleted.")


    def current_time(self) -> str:
        '''
        return current time in format "%Y/%m/%d %H:%M:%S" 
        '''

        structured_time = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        return structured_time


if __name__ == "__main__":
    model = Model()

