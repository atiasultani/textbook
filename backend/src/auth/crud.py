from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import datetime
from src.auth.models import User
from src.models.auth_session import AuthenticationSession as AuthSessionDB
from src.models.password_reset_token import PasswordResetToken as PasswordResetTokenDB
from src.models.oauth_account import OAuthAccount as OAuthAccountDB
from src.models.users import User as UserDB
from src.auth.schemas import UserCreate, UserUpdate
from src.auth.security import get_password_hash


# -------------------------
# User CRUD Operations
# -------------------------

def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    user_db = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user_db:
        return User.from_orm(user_db)
    return None


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    user_db = db.query(UserDB).filter(UserDB.email == email).first()
    if user_db:
        return User.from_orm(user_db)
    return None


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    users_db = db.query(UserDB).offset(skip).limit(limit).all()
    return [User.from_orm(u) for u in users_db]


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = UserDB(
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return User.from_orm(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )


def update_user(db: Session, user_id: str, user_update: UserUpdate) -> Optional[User]:
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        return None

    if user_update.name is not None:
        db_user.name = user_update.name
    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.profile_picture_url is not None:
        db_user.profile_picture_url = user_update.profile_picture_url

    db.commit()
    db.refresh(db_user)
    return User.from_orm(db_user)


def delete_user(db: Session, user_id: str) -> bool:
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True


def update_user_last_login(db: Session, user_id: str, last_login_at: Optional[datetime] = None) -> Optional[User]:
    if last_login_at is None:
        last_login_at = datetime.utcnow()
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        return None
    db_user.last_login_at = last_login_at
    db.commit()
    db.refresh(db_user)
    return User.from_orm(db_user)


def verify_user(db: Session, user_id: str) -> Optional[User]:
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        return None
    db_user.is_verified = True
    db.commit()
    db.refresh(db_user)
    return User.from_orm(db_user)


def deactivate_user(db: Session, user_id: str) -> Optional[User]:
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        return None
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    return User.from_orm(db_user)


def activate_user(db: Session, user_id: str) -> Optional[User]:
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        return None
    db_user.is_active = True
    db.commit()
    db.refresh(db_user)
    return User.from_orm(db_user)


# -------------------------
# Authentication Session CRUD
# -------------------------

def create_auth_session(db: Session, user_id: str, access_token: str, refresh_token_hash: str,
                       access_token_expires_at: datetime, refresh_token_expires_at: datetime,
                       user_agent: Optional[str] = None, ip_address: Optional[str] = None) -> AuthSessionDB:
    db_session = AuthSessionDB(
        user_id=user_id,
        access_token=access_token,
        refresh_token_hash=refresh_token_hash,
        access_token_expires_at=access_token_expires_at,
        refresh_token_expires_at=refresh_token_expires_at,
        user_agent=user_agent,
        ip_address=ip_address
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_auth_session_by_id(db: Session, session_id: str) -> Optional[AuthSessionDB]:
    return db.query(AuthSessionDB).filter(AuthSessionDB.id == session_id).first()


def get_auth_session_by_user_id(db: Session, user_id: str) -> List[AuthSessionDB]:
    return db.query(AuthSessionDB).filter(AuthSessionDB.user_id == user_id).all()


def get_auth_session_by_access_token(db: Session, access_token: str) -> Optional[AuthSessionDB]:
    return db.query(AuthSessionDB).filter(AuthSessionDB.access_token == access_token).first()


def update_auth_session_last_used(db: Session, session_id: str) -> Optional[AuthSessionDB]:
    db_session = db.query(AuthSessionDB).filter(AuthSessionDB.id == session_id).first()
    if not db_session:
        return None
    db_session.last_used_at = datetime.utcnow()
    db.commit()
    db.refresh(db_session)
    return db_session


def deactivate_auth_session(db: Session, session_id: str) -> bool:
    db_session = db.query(AuthSessionDB).filter(AuthSessionDB.id == session_id).first()
    if not db_session:
        return False
    db_session.is_active = False
    db.commit()
    return True


def delete_auth_session(db: Session, session_id: str) -> bool:
    db_session = db.query(AuthSessionDB).filter(AuthSessionDB.id == session_id).first()
    if not db_session:
        return False
    db.delete(db_session)
    db.commit()
    return True


# -------------------------
# Password Reset CRUD
# -------------------------

def create_password_reset_token(db: Session, user_id: str, token_hash: str,
                                expires_at: datetime, ip_address: str, user_agent: str) -> PasswordResetTokenDB:
    db_token = PasswordResetTokenDB(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_password_reset_token_by_token_hash(db: Session) -> Optional[PasswordResetTokenDB]:
    return (
        db.query(PasswordResetTokenDB)
        .filter(PasswordResetTokenDB.used_at.is_(None))
        .order_by(PasswordResetTokenDB.created_at.desc())
        .first()
    )


def mark_password_reset_token_as_used(db: Session, token_id: str) -> bool:
    db_token = db.query(PasswordResetTokenDB).filter(PasswordResetTokenDB.id == token_id).first()
    if not db_token:
        return False
    db_token.used_at = datetime.utcnow()
    db.commit()
    return True


def delete_expired_password_reset_tokens(db: Session) -> int:
    expired_tokens = db.query(PasswordResetTokenDB).filter(
        PasswordResetTokenDB.expires_at < datetime.utcnow()
    ).all()
    count = len(expired_tokens)
    for token in expired_tokens:
        db.delete(token)
    db.commit()
    return count


# -------------------------
# OAuth Account CRUD
# -------------------------

def create_oauth_account(db: Session, user_id: Optional[str], provider: str, provider_account_id: str,
                         email: str, name: str, access_token: str, refresh_token: Optional[str] = None,
                         expires_at: Optional[datetime] = None) -> OAuthAccountDB:
    db_oauth_account = OAuthAccountDB(
        user_id=user_id,
        provider=provider,
        provider_account_id=provider_account_id,
        email=email,
        name=name,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at
    )
    db.add(db_oauth_account)
    db.commit()
    db.refresh(db_oauth_account)
    return db_oauth_account


def get_oauth_account_by_provider_and_id(db: Session, provider: str, provider_account_id: str) -> Optional[OAuthAccountDB]:
    return db.query(OAuthAccountDB).filter(
        OAuthAccountDB.provider == provider,
        OAuthAccountDB.provider_account_id == provider_account_id
    ).first()
