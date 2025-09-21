'use client';
import React, { useState } from 'react';
import ConversationList from '../../../components/chat/ConversationList';
import ChatWindow from '../../../components/chat/ChatWindow';

const ChatPage = () => {
  const [selectedConversationId, setSelectedConversationId] = useState(null);

  return (
    <div className="chat-page">
      <ConversationList onSelectConversation={setSelectedConversationId} />
      <ChatWindow conversationId={selectedConversationId} />
    </div>
  );
};

export default ChatPage;
