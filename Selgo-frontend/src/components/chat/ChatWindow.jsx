import React, { useState, useEffect } from 'react';
import chatService from '../../services/chatService';

const ChatWindow = ({ conversationId }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  useEffect(() => {
    const fetchMessages = async () => {
      if (conversationId) {
        const fetchedMessages = await chatService.getMessages(conversationId);
        setMessages(fetchedMessages);
      }
    };
    fetchMessages();
  }, [conversationId]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (newMessage.trim() === '') return;

    try {
      const sentMessage = await chatService.sendMessage(conversationId, newMessage);
      setMessages([...messages, sentMessage]);
      setNewMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="chat-window">
      <div className="messages-list">
        {messages.map((message) => (
          <div key={message.id} className="message">
            <p>{message.content}</p>
            <span>{new Date(message.timestamp).toLocaleTimeString()}</span>
          </div>
        ))}
      </div>
      <form onSubmit={handleSendMessage} className="message-form">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default ChatWindow;
