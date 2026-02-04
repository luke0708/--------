from __future__ import annotations

from sqlmodel import Session, select

from app.auth import get_password_hash
from app.config import load_config
from app.database import engine, init_db
from app.models import User


def main() -> None:
    init_db()
    config = load_config()
    username = config.admin_username or "admin"
    password = config.admin_password or "change_me"

    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if user:
            user.password_hash = get_password_hash(password)
            user.role = "admin"
            session.add(user)
            session.commit()
            print(f"管理员已更新: {username}")
        else:
            user = User(
                username=username,
                password_hash=get_password_hash(password),
                role="admin",
            )
            session.add(user)
            session.commit()
            print(f"管理员已创建: {username}")


if __name__ == "__main__":
    main()
