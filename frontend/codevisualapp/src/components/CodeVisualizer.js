import React, { useState } from 'react';
import "./CodeVisalizer.css";

function CodeVisualizer() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() === '') return;

    // Update messages with new input
    setMessages([...messages, { text: input, sender: 'user' }]);
    setInput('');

    // Implement chatbot response logic here if needed
  };

  return (
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
  );
}

export default CodeVisualizer;
