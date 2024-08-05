# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Users
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Добавляем тестового пользователя
    test_user = Users(
        username="testuser",
        hashed_password=bcrypt_context.hash("testpassword")
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)
