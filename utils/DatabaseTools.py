import glob
import sqlite3
from os import getlogin as username
from datetime import datetime
import inspect
from logging import getLogger, exception
from logging import info as information
from logging import debug as debugging
import subprocess

class Tools:

    def __init__(self): 
        pass
    
    @staticmethod
    def createUserDB():
        """
        Create an sqlite3 database within the users .local directory and populate
        it with a table for logging chat messages.
    
        The table will consist of a X fields; username for logging who sent the
        message, subject for the general idea behind the message which can be set
        with a /command, a timestamp for when it was sent, and the text body
        of the message itself.
        """
    
        # Set up logging.
        getLogger()
     
        _name = inspect.stack()[0][3]
        _time = datetime.timestamp(datetime.now())
    
        debugging(#####} CONSTANTS
            f"{_time}:{_name}:Beginning constants setup."
        )
    
        # The users .local directory; see the Linux FS for info about that.
        local_directory = f"/home/{username()}/.local"
        debugging(f"{_time}:{_name}:    --Local Directory: ✅")
    
        # Filename and path for the sqlite database.
        lab_database = f"{local_directory}/lab-93.db"
        debugging(f"{_time}:{_name}:    --Lab Database: ✅")
    
        # Bash command for creating the .local directory.
        createSubDirectory = f"mkdir -p {local_directory} > /dev/null "
        debugging(f"{_time}:{_name}:    --Sub-Directory Shell String: ✅")
    
        # SQLite3 command for creating the messages table
        # with our required columns.
        createMessagesTable_SQL = (
            f"CREATE TABLE IF NOT EXISTS "
                f"messages("
                    f"username TEXT REQUIRED KEY, "
                    f"subject TEXT, "
                    f"timestamp REAL, "
                    f"message TEXT"
                f")"
        )
        debugging(f"{_time}:{_name}:    --Messages Table Creation SQL String: ✅")
    
        # Check for the .local directory and create it if need be.
        debugging(f"{_time}:{_name}:    --Validate Local Directory:")
    
        # If glob returns any results then the directory already exists.
        if len(glob(local_directory)) >= 1:
            debugging(f"{_time}:{_name}:      --Directory exists. ✅"); pass
    
        else:# If not, then the directory needs to be created.
            debugging(f"{_time}:{_name}:      --Directory does not exist; creating.")
    
            try: 
                subprocess.Run(# Execute the directory creation one-liner.
                createSubDirectory.split()
            ); information(
                f"{_time}:{_name}:      --Created subdirectory at {local_directory}"
            )
    
            # Log any mishaps and inform the caller.
            except Exception as error:
                exception(
                f"{_time}:{_name}:"
                f"There was an issue creating the .local subdirectory:\n"
                f"{error}"
            )


        # Begin sqlite database connection and initialize cursor.
        debugging(f"{_time}:{_name}:    --Attempting connection to database at {lab_database}")
        try:
            # Establish connection to .db file.
            connection = sqlite3.connect(lab_database); debugging(
                f"{_time}:{_name}:      --Connection established ✅"
            )

            # Create cursor and lable it for execution.
            cursor = connection.cursor(); execute = cursor.execute; debugging(
                f"{_time}:{_name}:      --Cursor successfully labelled ✅"
            )

            # Run the table creation sql and save your work!
            while True: 
                cursor.execute(
                    createMessagesTable_SQL
                ); information(
                    f"{_time}:{_name}:"
                    f"Messages table successfully created for user {username()}"
                ); connection.commit(); break

        # Handle any errors gracefully, and inform the caller.
        except Exception as error:
            exception(
                f"{_time}:{_name}:"
                f"There was an issue creating a messages table "
                f"within the user database;\n{error}"
            )

            return error