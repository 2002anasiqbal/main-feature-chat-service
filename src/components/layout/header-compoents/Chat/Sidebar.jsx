"use client";
import React from "react";
import ConversationListItem from "./ConversationListItem";

const Sidebar = ({ conversations, searchTerm, onSearchChange, onSelectChat, selectedChat }) => {
  const filteredConversations = conversations.filter((convo) =>
    convo.sender.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="bg-white border-r border-gray-200 h-full overflow-y-auto flex flex-col">
      {/* Search Bar */}
      <div className="p-3 flex-shrink-0">
        <div className="flex items-center bg-gray-100 rounded-full p-2">
          <input
            type="text"
            className="bg-transparent flex-grow outline-none text-sm text-gray-700 placeholder-gray-500"
            placeholder="Search..."
            value={searchTerm}
            onChange={onSearchChange}
          />
          <div className="ml-2">
            <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
        </div>
      </div>
      {/* Conversation List */}
      <div className="overflow-y-auto flex-1">
        {filteredConversations.map((convo, index) => (
          <ConversationListItem
            key={index}
            convo={convo}
            index={index}
            isSelected={selectedChat === index}
            onSelect={onSelectChat}
          />
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
