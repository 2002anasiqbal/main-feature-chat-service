"use client";
import React, { useState, useRef, useEffect } from "react";
import useAuthStore from "@/store/store";
import { mockUsers } from "@/utils/mockUsers";
import Sidebar from "./Chat/Sidebar";
import ChatWindow from "./Chat/ChatWindow";

export default function Messages() {
  const { user, fetchUser, isAuthenticated } = useAuthStore();
  const [conversations, setConversations] = useState([]);
  const [selectedChat, setSelectedChat] = useState(0);
  const [mobileView, setMobileView] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [message, setMessage] = useState("");
  const messagesEndRef = useRef(null);

  // Transform chats for UI use.
  const transformChats = (loggedInUserName, chatArray) =>
    chatArray.map((chat) => {
      const otherParticipant =
        chat.participants.find((p) => p !== loggedInUserName) || "Unknown";
      return {
        sender: otherParticipant,
        messages: chat.messages,
      };
    });

  // Fetch user and chats on mount/user change.
  useEffect(() => {
    (async () => {
      await fetchUser();
      if (isAuthenticated() && user?.email) {
        const foundUser = mockUsers.find((u) => u.email === user.email);
        if (foundUser && foundUser.chats) {
          const transformed = transformChats(foundUser.name, foundUser.chats);
          setConversations(transformed);
        } else {
          setConversations([]);
        }
      } else {
        setConversations([]);
      }
    })();
  }, [fetchUser, isAuthenticated, user?.email]);

  // Auto-scroll to the bottom on new messages.
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [conversations]);

  // Handle chat selection.
  const handleChatSelect = (index) => {
    setSelectedChat(index);
    setMobileView(false);
  };

  const handleBackButton = () => {
    setMobileView(true);
  };

  // Send a new message.
  const handleSendMessage = () => {
    if (!message.trim()) return;
    const newMessage = {
      text: message,
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      isSender: true,
    };

    const updated = [...conversations];
    updated[selectedChat] = {
      ...updated[selectedChat],
      messages: [...updated[selectedChat].messages, newMessage],
    };

    setConversations(updated);
    setMessage("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (!isAuthenticated() || conversations.length === 0) {
    return (
      <div className="flex h-full items-center justify-center bg-gray-100">
        <p className="text-gray-600">No messages for you.</p>
      </div>
    );
  }

  return (
    <div className="flex h-full w-full bg-gray-100">
      {/* Sidebar: shown on mobile if mobileView is true and always on desktop */}
      <div className={`${mobileView ? "block w-full" : "hidden"} md:block md:w-80 h-full`}>
        <Sidebar
          conversations={conversations}
          searchTerm={searchTerm}
          onSearchChange={(e) => setSearchTerm(e.target.value)}
          onSelectChat={handleChatSelect}
          selectedChat={selectedChat}
        />
      </div>

      {/* Chat Window: shown on mobile when a chat is selected and always on desktop */}
      <div className={`${mobileView ? "hidden" : "block w-full"} md:block md:flex-1 h-full`}>
        <ChatWindow
          conversation={conversations[selectedChat]}
          messagesEndRef={messagesEndRef}
          message={message}
          setMessage={setMessage}
          handleSendMessage={handleSendMessage}
          handleKeyPress={handleKeyPress}
          handleBackButton={handleBackButton}
        />
      </div>
    </div>
  );
}