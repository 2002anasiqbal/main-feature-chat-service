import React, { useState, useEffect } from 'react';
import chatService from '../../services/chatService';

const ConversationList = ({ onSelectConversation }) => {
  const [conversations, setConversations] = useState([]);

  useEffect(() => {
    const fetchConversations = async () => {
      const fetchedConversations = await chatService.getConversations();
      setConversations(fetchedConversations);
    };
    fetchConversations();
  }, []);

  return (
    <div className="conversation-list">
      <h2>Conversations</h2>
      {conversations.map((conversation) => (
        <div
          key={conversation.id}
          className="conversation-item"
          onClick={() => onSelectConversation(conversation.id)}
        >
          <p>Conversation with {conversation.participants.map(p => p.user_id).join(', ')}</p>
        </div>
      ))}
    </div>
  );
};

export default ConversationList;
