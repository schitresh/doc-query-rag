import typing as t

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.folders import repo
from app.folders.schemas import FolderCreate, FolderResponse

router = APIRouter(prefix="/folders", tags=["Folders"])

DatabaseDependency = t.Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[FolderResponse])
def list_folders(db: DatabaseDependency = None):
    return repo.list_folders(db)


@router.post("", response_model=FolderCreate)
def create_folder(name: str, db: DatabaseDependency = None):
    return repo.create_folder(db, name)
