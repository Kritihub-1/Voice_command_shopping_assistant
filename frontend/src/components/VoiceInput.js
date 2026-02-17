import React, { useState, useRef } from 'react';
import { FaMicrophone, FaStop } from 'react-icons/fa';
import '../styles/VoiceInput.css';

const VoiceInput = ({ onCommand, loading }) => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const recognitionRef = useRef(null);

  const initSpeechRecognition = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Speech Recognition not supported in this browser');
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      setIsListening(true);
      setTranscript('');
    };

    recognition.onresult = (event) => {
      let interim = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcriptSegment = event.results[i][0].transcript;
        interim += transcriptSegment;
      }
      setTranscript(interim);
    };

    recognition.onend = () => {
      setIsListening(false);
      if (transcript.trim()) {
        onCommand(transcript);
        setTranscript('');
      }
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setIsListening(false);
    };

    recognitionRef.current = recognition;
  };

  const startListening = () => {
    if (!recognitionRef.current) {
      initSpeechRecognition();
    }
    recognitionRef.current.start();
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
  };

  return (
    <div className="voice-input">
      <div className="voice-container">
        {isListening ? (
          <>
            <button 
              className="voice-btn recording"
              onClick={stopListening}
              title="Stop listening"
            >
              <FaStop size={24} />
            </button>
            <div className="listening-indicator">
              <span className="pulse"></span>
              Listening...
            </div>
          </>
        ) : (
          <button 
            className="voice-btn"
            onClick={startListening}
            disabled={loading}
            title="Click to start speaking"
          >
            <FaMicrophone size={24} />
          </button>
        )}
      </div>
      
      {transcript && (
        <div className="transcript">
          <p>{transcript}</p>
        </div>
      )}
      
      <p className="voice-hint">
        Say things like: "Add milk", "I need bread", "Remove apples"
      </p>
    </div>
  );
};

export default VoiceInput;
