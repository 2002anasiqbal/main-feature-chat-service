const jwt = require("jsonwebtoken");

const mockToken = jwt.sign(
  { id: 2, name: "John", email: "a@a.com" },
  "your_secret_key", // Change this to a real secret key in production
  { expiresIn: "1h" } // Token expires in 1 hour
);

console.log("Generated Mock Token:", mockToken);