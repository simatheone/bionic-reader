
import uuid
from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class Document(Base):
    """The Document model."""
    __tablename__ = 'document'

    title = Column(
        String(256), default='Untitled Document', nullable=False
    )
    text = Column(Text, default='Enter your text', nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
            'user.id', ondelete='CASCADE', name='fk_document_user_id_user'
        ), nullable=False
    )

    def __repr__(self):
        return (
            f'Document: {self.title}, created at: {self.created_at}'
        )


class User(SQLAlchemyBaseUserTableUUID, Base):
    first_name = Column(String(128), nullable=False)
