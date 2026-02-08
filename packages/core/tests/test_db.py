from core.db.connection import SessionLocal
from core.db.models import User

db = SessionLocal()

def test_create_user():
    user = User(first_name="test", last_name="user", email="user@test.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    persisted_user = db.query(User).filter_by(first_name="test").first()
    assert persisted_user is not None
    assert persisted_user.id is not None
    assert persisted_user.first_name == "test"
    assert persisted_user.last_name == "user"
    assert persisted_user.email == "user@test.com"

    db.delete(persisted_user)
    db.commit()
    db.close()  