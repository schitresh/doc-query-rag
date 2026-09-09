from sqlalchemy.orm import Session

from app.folders.models import Folder


def create_folder(db: Session, name: str) -> Folder:
    folder = Folder(name=name)
    db.add(folder)
    db.commit()
    db.refresh(folder)
    return folder


def list_folders(db: Session) -> list[Folder]:
    return db.query(Folder).all()


def get_folders_by_id(db: Session, folder_id: int) -> Folder | None:
    return db.query(Folder).filter_by(id=folder_id).first()
