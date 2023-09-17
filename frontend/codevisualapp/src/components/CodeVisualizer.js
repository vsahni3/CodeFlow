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

    // Add the new message to the top of the messages array
    setMessages([{ text: input, sender: 'user' }, ...messages]);
    setInput('');

    // Implement chatbot response logic here if needed
  };

  return (
    <div className="chat-visual-container">
      {/* Visual Screen */}
      <div className="visual-screen">
        
        {/* For example, you can add an image or any visual elements */}
      </div>

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
