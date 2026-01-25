from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import Integer, BigInteger, String, DateTime, Boolean, Text, ForeignKey
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Debate(Base):
    __tablename__ = "debate"

    debate_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="debate")

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

class Message(Base):
    __tablename__ = "message"

    message_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    debate_id: Mapped[int] = mapped_column(Integer, ForeignKey('debate.debate_id'))
    
    debate: Mapped["Debate"] = relationship("Debate", back_populates="messages")

    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    text: Mapped[str] = mapped_column(Text, nullable=True)

    state: Mapped[str] = mapped_column(String(15), nullable=False)

    addet_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    
    from_username: Mapped[str] = mapped_column(String(255), default="Пользователь")