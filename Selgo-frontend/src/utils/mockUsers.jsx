// /src/utils/mockUsers.js

export const mockUsers = [
    {
      id: 1,
      name: "Hassan",
      email: "hassan@example.com",
      password: "123456",
      token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwibmFtZSI6Ikhhc3NhbiIsImVtYWlsIjoiaGFzc2FuQGV4YW1wbGUuY29tIiwiaWF0IjoxNzQxODE4MTY1LCJleHAiOjE3NDE4MjE3NjV9.qDJguR-YmSY7DohQKE6WQfHP87V-1aHBKIy8quBfOt8", // Example JWT
      chats: [
        {
          chatId: 101,
          participants: ["Hassan", "Auria"],
          messages: [
            { text: "Hey Hassan, how's your day?", time: "09:15", isSender: false },
            { text: "Morning Auria! I'm doing great, thanks!", time: "09:16", isSender: true },
          ],
        },
        {
          chatId: 102,
          participants: ["Hassan", "John"],
          messages: [
            { text: "Hassan, can we meet tomorrow?", time: "10:30", isSender: false },
            { text: "Sure, John. Let's do 2pm.", time: "10:31", isSender: true },
          ],
        },
      ],
    },
    {
      id: 2,
      name: "John Doe",
      email: "a@a.com",
      password: "123456",
      token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwibmFtZSI6IkpvaG4iLCJlbWFpbCI6ImFAYS5jb20iLCJpYXQiOjE3NDE4MjY0MzgsImV4cCI6MTc0MTgzMDAzOH0.Jpg26mTlUKIg68ygSUoErnPaO1pY8kM-y6-Jk3NjzYs",
      chats: [
        {
          chatId: 202,
          participants: ["John", "Alice"],
          messages: [
            { text: "Hi John, any update on the project?", time: "08:20", isSender: false },
            { text: "Should be done by tomorrow.", time: "08:22", isSender: true },
          ],
        },
        {
          chatId: 102, // Same conversation as Hassan's ID 102, from John's POV
          participants: ["Hassan", "John"],
          messages: [
            { text: "Hassan, can we meet tomorrow?", time: "10:30", isSender: true },
            { text: "Sure, John. Let's do 2pm.", time: "10:31", isSender: false },
          ],
        },
      ],
    },
  ];
  