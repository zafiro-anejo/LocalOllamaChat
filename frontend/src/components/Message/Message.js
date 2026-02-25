import React from 'react';
import styles from './Message.module.css';
import userLogo from '../../res/userLogo.png';
import botLogo from '../../res/ollamaLogo.png';

const Message = ({ role, content }) => {
  const isUser = role === 'user';
  return (
    <div className={`${styles.message} ${isUser ? styles.user : styles.bot}`}>
      <div className={styles.avatar}>
        <img 
          src={isUser ? userLogo : botLogo} 
          alt={isUser ? 'User' : 'Bot'} 
          className={styles.avatarImage}
        />
      </div>
      <div className={styles.bubble}>
        <div className={styles.content}>{content}</div>
      </div>
    </div>
  );
};

export default Message;