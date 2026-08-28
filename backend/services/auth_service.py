from sqlalchemy.orm import Session

from backend.models.company import Company
from backend.models.user import User

from backend.schemas.auth import (
    CompanyRegisterRequest,
    LoginRequest,
)

from backend.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class AuthService:

    @staticmethod
    def register_company(
        request: CompanyRegisterRequest,
        db: Session,
    ):

        existing_user = (
            db.query(User)
            .filter(User.email == request.admin_email)
            .first()
        )

        if existing_user:
            raise ValueError("Email already registered")

        company = Company(
            name=request.company_name,
            industry=request.industry,
            email=request.admin_email,
        )

        db.add(company)
        db.flush()

        admin = User(
            company_id=company.id,
            full_name=request.admin_name,
            email=request.admin_email,
            password_hash=hash_password(request.password),
            role="admin",
        )

        db.add(admin)
        db.commit()

        return {
            "message": "Company registered successfully",
            "company_id": company.id,
            "admin_user_id": admin.id,
        }

    @staticmethod
    def login(
        request: LoginRequest,
        db: Session,
    ):

        user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if user is None:
            raise ValueError("Invalid email or password")

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise ValueError("Invalid email or password")

        access_token = create_access_token(
            {
                "sub": user.email,
                "user_id": user.id,
                "company_id": user.company_id,
                "role": user.role,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
