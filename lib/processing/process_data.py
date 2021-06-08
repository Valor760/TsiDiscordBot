from lib.db import db
from ..cogs.creatorOnly import creatorOnly
from discord.ext.commands import Cog


class WebData():
    def __init__(self, user_id, st_code, st_name):
        self.user_id = user_id
        self.st_code = st_code
        self.st_name = st_name

    def process_data(self, user_id, st_code, st_name):

        if "st" in st_code.lower():
            st_code = st_code.lower().replace("st", '')

        isThereCode = db.column("SELECT StudentCode FROM studentDB WHERE StudentCode = ?",
                      st_code)

        if isThereCode:
            if st_name == '':
                std_name = db.column("SELECT StudentName FROM studentDB WHERE StudentCode = ?",
                                        st_code)
                student_name = std_name[0]
            else:
                student_name = st_name

            student_group = db.column("SELECT GroupNum FROM studentDB WHERE StudentCode = ?",
                                      st_code)

            db.execute("UPDATE students SET StudentCode = ?, StudentName = ?, GroupNum = ? WHERE UserID = ?",
                       int(st_code), student_name, student_group[0], user_id)

            db.commit()

            # m = creatorOnly(Cog)
            # m.nickname_change(student_name, user_id)
            # Сделать передачу данных напрямую боту!!!


            return True

        else:
            return False
