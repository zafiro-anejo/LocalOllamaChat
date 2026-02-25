import React from 'react';
import useChat from './hooks/useChat';
import Message from './components/Message/Message';
import ChatInput from './components/ChatInput/ChatInput';
import TypingIndicator from './components/TypingIndicator/TypingIndicator';
import styles from './App.module.css';

function App() {
  const { messages, input, setInput, loading, sendMessage, clearMessages } = useChat();

  return (
    <div className={styles.app}>
      <div className={styles.chatContainer}>
        <div className={styles.messages}>
          {messages.map((msg, idx) => (
            <Message key={idx} role={msg.role} content={msg.content} />
          ))}
          {loading && <TypingIndicator />}
        </div>
        <div className={styles.inputWrapper}>
          <ChatInput
            input={input}
            setInput={setInput}
            loading={loading}
            onSend={sendMessage}
            onClear={clearMessages}
          />
        </div>
      </div>
    </div>
  );
}

export default App;