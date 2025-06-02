"use client";
import React from "react";

const ConversationListItem = ({ convo, index, isSelected, onSelect }) => {
  const lastMsg = convo.messages[convo.messages.length - 1];
  const lastTime = lastMsg?.time || "";
  return (
    <div
      onClick={() => onSelect(index)}
      className={`flex items-center p-4 cursor-pointer ${
        isSelected
          ? "bg-teal-600 text-white"
          : "bg-white text-gray-900 hover:bg-teal-400 hover:text-white"
      }`}
    >
      <div className="relative w-12 h-12">
        <div className="w-12 h-12 rounded-full overflow-hidden bg-gray-300 flex items-center justify-center">
          <span className="text-white font-bold">{convo.sender.charAt(0)}</span>
        </div>
      </div>
      <div className="ml-3 flex-grow">
        <div className="flex justify-between">
          <p className={`font-medium ${isSelected ? "text-white" : ""}`}>
            {convo.sender}
          </p>
          <p className={`text-xs ${isSelected ? "text-white" : "text-gray-500"}`}>
            {lastTime}
          </p>
        </div>
      </div>
    </div>
  );
};

export default ConversationListItem;
