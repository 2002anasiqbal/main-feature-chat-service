from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from ..models.chat_models import Conversation, Message, Participant
from ..models.chat_schemas import ConversationCreate, MessageCreate

class ChatRepository:
    @staticmethod
    def create_conversation(db: Session, conversation_data: ConversationCreate, user_id: int) -> Conversation:
        db_conversation = Conversation()
        db.add(db_conversation)
        db.commit()
        db.refresh(db_conversation)

        # Add participants
        participant1 = Participant(user_id=user_id, conversation_id=db_conversation.id)
        participant2 = Participant(user_id=conversation_data.participant_id, conversation_id=db_conversation.id)
        db.add_all([participant1, participant2])
        db.commit()
        db.refresh(db_conversation)

        return db_conversation

    @staticmethod
    def get_user_conversations(db: Session, user_id: int) -> List[Conversation]:
        return db.query(Conversation).join(Participant).filter(Participant.user_id == user_id).all()

    @staticmethod
    def get_conversation(db: Session, conversation_id: int, user_id: int) -> Optional[Conversation]:
        return db.query(Conversation).join(Participant).filter(
            Conversation.id == conversation_id,
            Participant.user_id == user_id
        ).first()

    @staticmethod
    def create_message(db: Session, conversation_id: int, message_data: MessageCreate, user_id: int) -> Optional[Message]:
        conversation = ChatRepository.get_conversation(db, conversation_id, user_id)
        if not conversation:
            return None

        db_message = Message(
            conversation_id=conversation_id,
            sender_id=user_id,
            content=message_data.content
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message

    @staticmethod
    def get_messages(db: Session, conversation_id: int, user_id: int) -> Optional[List[Message]]:
        conversation = ChatRepository.get_conversation(db, conversation_id, user_id)
        if not conversation:
            return None

        return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp.asc()).all()