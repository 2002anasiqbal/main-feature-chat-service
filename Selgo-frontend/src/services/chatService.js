const API_URL = process.env.NEXT_PUBLIC_CHAT_API_URL || 'http://localhost:8002/api/v1';

import { apiClient } from './authService';

const chatService = {
  createConversation: async (participantId) => {
    try {
      const response = await apiClient.post('/chats/conversations', { participant_id: participantId });
      return response.data;
    } catch (error) {
      console.error('Error creating conversation:', error);
      throw error;
    }
  },

  getConversations: async () => {
    try {
      const response = await apiClient.get('/chats/conversations');
      return response.data;
    } catch (error) {
      console.error('Error fetching conversations:', error);
      return [];
    }
  },

  getMessages: async (conversationId) => {
    try {
      const response = await apiClient.get(`/chats/conversations/${conversationId}/messages`);
      return response.data;
    } catch (error) {
      console.error('Error fetching messages:', error);
      return [];
    }
  },

  sendMessage: async (conversationId, content) => {
    try {
      const response = await apiClient.post(`/chats/conversations/${conversationId}/messages`, { content });
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },
};

export default chatService;
