from src.commands.base_command import BaseCommand
from src.models import db
from src.errors.errors import ApiError
class ClearDatabase(BaseCommand):
    def execute(self):
        try:
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                print(f'Clearing table {table}')
                db.session.execute(table.delete())
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ApiError()