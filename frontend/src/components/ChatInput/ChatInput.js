import React, { useRef, useEffect } from 'react';
import styles from './ChatInput.module.css';

const ChatInput = ({ input, setInput, loading, onSend, onClear }) => {
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!loading && input.trim()) {
        onSend();
      }
    }
  };

  const handleChange = (e) => {
    setInput(e.target.value);
  };

  return (
    <div className={styles.container}>
      <button
        onClick={onClear}
        className={styles.clearButton}
        title="Очистить чат"
        disabled={loading}
      >
        ✕
      </button>
      <textarea
        ref={textareaRef}
        value={input}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        placeholder="Введите ваш вопрос..."
        disabled={loading}
        className={styles.textarea}
        rows={1}
      />
      <button
        onClick={onSend}
        disabled={loading || !input.trim()}
        className={styles.button}
      >
        {loading ? '...' : '➤'}
      </button>
    </div>
  );
};

export default ChatInput;