import React from 'react';
import styles from './TypingIndicator.module.css';
import botLogo from '../../res/ollamaLogo.png';

const TypingIndicator = () => {
  return (
    <div className={`${styles.message} ${styles.bot}`}>
      <div className={styles.avatar}>
        <img 
          src={botLogo} 
          alt="Bot" 
          className={styles.avatarImage}
        />
      </div>
      <div className={styles.bubble}>
        <div className={styles.typing}>
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;