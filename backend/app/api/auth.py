"""Authentication API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.models import User, UserSettings
from app.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    UserSettingsUpdate,
    UserSettingsResponse,
)
from app.core.security import verify_password, get_password_hash, encrypt_value, decrypt_value
from app.core.auth import create_access_token, create_refresh_token
from app.dependencies import get_current_user
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        Created user object

    Raises:
        HTTPException: If email already exists
    """
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create default user settings
    user_settings = UserSettings(user_id=user.id)
    db.add(user_settings)
    db.commit()

    return user


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login and receive JWT tokens.

    Args:
        credentials: Login credentials
        db: Database session

    Returns:
        Access and refresh tokens

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    # Create tokens
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information.

    Args:
        current_user: Current authenticated user

    Returns:
        User information
    """
    return current_user


@router.get("/settings", response_model=UserSettingsResponse)
async def get_user_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user settings (without sensitive data).

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        User settings (masked sensitive fields)
    """
    user_settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()

    if not user_settings:
        # Create default settings if not exists
        user_settings = UserSettings(user_id=current_user.id)
        db.add(user_settings)
        db.commit()
        db.refresh(user_settings)

    # Return masked response
    return UserSettingsResponse(
        user_id=user_settings.user_id,
        gmail_address=user_settings.gmail_address,
        telegram_chat_id=user_settings.telegram_chat_id,
        notification_method=user_settings.notification_method,
        has_gemini_api_key=bool(user_settings.gemini_api_key),
        has_gmail_app_password=bool(user_settings.gmail_app_password),
        has_telegram_bot_token=bool(user_settings.telegram_bot_token),
        created_at=user_settings.created_at,
        updated_at=user_settings.updated_at,
    )


@router.put("/settings", response_model=UserSettingsResponse)
async def update_user_settings(
    settings_data: UserSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user settings (API keys and credentials).

    Args:
        settings_data: Settings update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated user settings (masked)
    """
    user_settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()

    if not user_settings:
        user_settings = UserSettings(user_id=current_user.id)
        db.add(user_settings)

    # Update fields (encrypt sensitive data)
    update_data = settings_data.model_dump(exclude_unset=True)

    if "gemini_api_key" in update_data and update_data["gemini_api_key"]:
        user_settings.gemini_api_key = encrypt_value(update_data["gemini_api_key"])

    if "gmail_address" in update_data:
        user_settings.gmail_address = update_data["gmail_address"]

    if "gmail_app_password" in update_data and update_data["gmail_app_password"]:
        user_settings.gmail_app_password = encrypt_value(update_data["gmail_app_password"])

    if "telegram_bot_token" in update_data and update_data["telegram_bot_token"]:
        user_settings.telegram_bot_token = encrypt_value(update_data["telegram_bot_token"])

    if "telegram_chat_id" in update_data:
        user_settings.telegram_chat_id = update_data["telegram_chat_id"]

    if "notification_method" in update_data:
        user_settings.notification_method = update_data["notification_method"]

    db.commit()
    db.refresh(user_settings)

    # Return masked response
    return UserSettingsResponse(
        user_id=user_settings.user_id,
        gmail_address=user_settings.gmail_address,
        telegram_chat_id=user_settings.telegram_chat_id,
        notification_method=user_settings.notification_method,
        has_gemini_api_key=bool(user_settings.gemini_api_key),
        has_gmail_app_password=bool(user_settings.gmail_app_password),
        has_telegram_bot_token=bool(user_settings.telegram_bot_token),
        created_at=user_settings.created_at,
        updated_at=user_settings.updated_at,
    )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout user (client should discard tokens).

    Args:
        current_user: Current authenticated user

    Returns:
        Success message
    """
    # In a stateless JWT setup, logout is handled client-side
    # For stateful approach, implement token blacklist
    return {"message": "Successfully logged out"}
