"use client";
import React from "react";
import ChatHeader from "./ChatHeader";
import ChatMessages from "./ChatMessages";
import ChatInput from "./ChatInput";

const ChatWindow = ({
  conversation,
  messagesEndRef,
  message,
  setMessage,
  handleSendMessage,
  handleKeyPress,
  handleBackButton,
}) => {
  return (
    <div className="flex flex-col h-full w-full">
      {/* Chat Header with mobile back button */}
      <ChatHeader sender={conversation.sender} handleBackButton={handleBackButton} />

      {/* Scrollable messages area */}
      <div className="flex-1 overflow-y-auto bg-gray-50">
        <div className="p-4">
          <ChatMessages messages={conversation.messages} />
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input bar */}
      <ChatInput
        message={message}
        setMessage={setMessage}
        handleSendMessage={handleSendMessage}
        handleKeyPress={handleKeyPress}
      />
    </div>
  );
};

export default ChatWindow;