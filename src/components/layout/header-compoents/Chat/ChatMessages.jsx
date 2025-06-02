"use client";
import React from "react";

const ChatMessages = ({ messages }) => {
  return (
    <>
      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={`flex ${msg.isSender ? "justify-end" : "justify-start"} mb-4`}
        >
          {msg.isSender ? (
            <div className="flex flex-col items-end">
              <div className="max-w-md px-4 py-2 rounded-lg bg-teal-600 text-white">
                <p>{msg.text}</p>
              </div>
              <span className="text-xs text-gray-500 mt-1">{msg.time}</span>
            </div>
          ) : (
            <div className="flex flex-col items-start">
              <div className="max-w-md px-4 py-2 rounded-lg bg-gray-200 text-gray-800">
                <p>{msg.text}</p>
              </div>
              <span className="text-xs text-gray-500 mt-1">{msg.time}</span>
            </div>
          )}
        </div>
      ))}
    </>
  );
};

export default ChatMessages;
