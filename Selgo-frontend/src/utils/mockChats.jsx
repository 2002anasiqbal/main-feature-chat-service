  export const mockFetchChats = (email) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        // Find the user’s chats if they exist
        const userChat = mockChats.find((c) => c.userEmail === email);
        if (userChat) {
          resolve({ chats: userChat.conversations });
        } else {
          resolve({ chats: [] });
        }
      }, 500); // 500ms simulated delay
    });
  };  