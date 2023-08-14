"""
"""
# notes from the web.

import argparse
import sqlite3

class Notes:
    """ """
    def __init__(self):
        self._db_name = "notes.db" # Convention: Private variable.
        self.conn = sqlite3.connect(self._db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        """ close web """
        self.cursor.close()
        self.conn.close()

    def get_notes(self):
        """ get notes """
        self.cursor.execute("select * from notes")
        results = self.cursor.fetchall()
        # [(1, "content", "2020-11-12 12:34:56"), ...]
        return results

    def print_notes(self):
        """ print notes """
        for id, content, date in self.get_notes():
            print(f"[{id}] Note saved on {date}")
            print(content, end="\n\n")

    def get_note(self, note_id):
        """Get a single note matching the note_id"""
        sql = "select * from notes where id = ?"
        values = (note_id, )
        self.cursor.execute(sql, values)
        tup = self.cursor.fetchone()
        return {
            "id": tup[0],
            "content": tup[1],
            "created_on": tup[2],
        }

    def add_note(self, content):
        """ add note """
        sql = "insert into notes (content) values (?)"
        values = (content, )
        self.cursor.execute(sql, values)
        self.conn.commit()
        print("Note saved.")

    def remove_note(self, id):
        """ remove note """
        sql = "delete from notes where id=?"
        values = (id, )
        self.cursor.execute(sql, values)
        self.conn.commit()
        print(f"Note {id} removed")


if __name__ == "__main__":
    # See the argpase docs at: https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(description='Do stuff with notes')
    parser.add_argument(
        '-d', '--delete', action='store', type=int,
        default=None,
        help='Specify the ID of the note to delete'
    )
    parser.add_argument(
        '-c', '--content', type=str,
        default=None,
        help="The content of the note to add"
    )
    args = parser.parse_args()

    # Create a Notes object (or instance)
    notes = Notes()
    if args.content is not None:
        notes.add_note(args.content)
    elif args.delete is not None:
        notes.remove_note(args.delete)
    else:
        notes.print_notes()
    notes.close()
