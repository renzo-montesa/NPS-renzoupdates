from extensions import db


class UploadFileModel(db.Model):
    __bind_key__ = 'client_db'
    __tablename__ = 'upload_file'

    id = db.Column(db.Integer, primary_key = True)
    file_uid = db.Column(db.String(32))
    fullpath = db.Column(db.String(255))
    filename = db.Column(db.String(255))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_in_db(self):
        db.session.delete(self)
        db.session.commit()

    def close(self):
        db.session.close()
