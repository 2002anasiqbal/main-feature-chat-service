from sqlalchemy.orm import Session
from typing import List, Optional

from ..repositories.repositories import ChatRepository
from ..models.chat_models import Conversation, Message
from ..models.chat_schemas import ConversationCreate, MessageCreate

class ChatService:
    @staticmethod
    def create_conversation(db: Session, conversation_data: ConversationCreate, user_id: int) -> Conversation:
        return ChatRepository.create_conversation(db, conversation_data, user_id)

    @staticmethod
    def get_user_conversations(db: Session, user_id: int) -> List[Conversation]:
        return ChatRepository.get_user_conversations(db, user_id)

    @staticmethod
    def get_conversation(db: Session, conversation_id: int, user_id: int) -> Optional[Conversation]:
        return ChatRepository.get_conversation(db, conversation_id, user_id)

    @staticmethod
    def create_message(db: Session, conversation_id: int, message_data: MessageCreate, user_id: int) -> Optional[Message]:
        return ChatRepository.create_message(db, conversation_id, message_data, user_id)

    @staticmethod
    def get_messages(db: Session, conversation_id: int, user_id: int) -> Optional[List[Message]]:
        return ChatRepository.get_messages(db, conversation_id, user_id)