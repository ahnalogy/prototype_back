from sqlalchemy.orm import Session
from app.model.domain.store import Store
from app.model.schema.store import StoreCreate


def get_store(db: Session, store_id: int):
    return db.query(Store).filter(Store.id == store_id).first()

def get_store_by_name(db: Session, name: str):
    return db.query(Store).filter(Store.name == name).first()   

def get_store_by_business_number(db: Session, business_number: int):
    return db.query(Store).filter(Store.business_number == business_number).first()

def get_stores(db: Session,user_id: int):
    return db.query(Store).filter(Store.user_id == user_id).all()

def get_stores_all(db: Session):
    return db.query(Store).all()

def get_stores_by_platform(db: Session, platform_id: int):
    return db.query(Store).filter(Store.platform_id == platform_id).all()

def create_store(db: Session, store: StoreCreate, user_id: int):
    db_store = Store(
        name=store.name,
        business_number=store.business_number,
        user_id=user_id  # Assuming user_id is part of StoreCreate
    )
    db.add(db_store)
    db.commit()  # Commit the transaction to save the new store
    db.refresh(db_store)
    return db_store

def delete_store(db: Session, store_id: int):
    store = get_store(db, store_id)
    if store:
        db.delete(store)
        db.commit()
        return True
    return False