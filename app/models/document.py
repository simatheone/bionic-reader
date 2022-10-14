from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.core.db import Base


class Document(Base):
    """The Document model."""
    title = Column(
        String(256), default='Untitled Document', nullable=False
    )
    text = Column(Text, nullable=False)
    create_date = Column(DateTime, default=datetime.now, nullable=False)
    user_id = Column(Integer, ForeignKey(
        'user.id', name='fk_document_user_id_user'
        ), nullable=False
    )

    def __repr__(self):
        return f'Created document: {self.title}'
