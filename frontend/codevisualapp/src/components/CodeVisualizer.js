import React, { useState } from 'react';
import './CodeVisualizer.css';

function CodeVisualizer() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() === '') return;

    // Add the user's message to the chat
    setMessages((prevMessages) => [{ text: input, sender: 'user' }, ...prevMessages]);
    setInput('');

    // Simulate a chatbot response (you can replace this with your actual chatbot logic)
    simulateChatbotResponse('h1');
  };

  const simulateChatbotResponse = (userInput) => {
    // Here, you can implement your chatbot logic to generate a response based on the user's input.
    // For simplicity, let's just echo back the user's input for demonstration purposes.
    const botResponse = `You said: ${userInput}`;

    // Add the chatbot's response to the chat
    setMessages((prevMessages) => [{ text: botResponse, sender: 'bot' }, ...prevMessages]);
  };

  return (
    <div className="chat-visual-container">
      {/* Chat Box */}
      <div className="chat-box">
        {/* Previous Messages */}
        <div className="previous-messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              {message.text}
            </div>
          ))}
        </div>

        {/* Text Input and Submit Button */}
        <form onSubmit={handleSubmit} className="message-input-form">
          {/* Text Input */}
          <input
            type="text"
            value={input}
            onChange={handleInputChange}
            placeholder="Type your message..."
          />

          {/* Submit Button */}
          <button type="submit">Send</button>
        </form>
      </div>
    </div>
  );
}

export default CodeVisualizer;
