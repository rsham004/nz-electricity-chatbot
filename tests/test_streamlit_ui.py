import pytest
from unittest.mock import Mock, patch, MagicMock
import streamlit as st

# Tests for Streamlit UI components


class TestStreamlitUI:
    """Test Streamlit chat interface."""
    
    def test_chat_interface_initialization(self):
        """Test chat interface initializes correctly."""
        from src.ui.chat_interface import initialize_chat
        
        # Create a mock session state object
        mock_session = MagicMock()
        mock_session.__contains__ = lambda self, key: False  # Initially empty
        
        with patch.object(st, 'session_state', mock_session):
            initialize_chat()
            
            # Check that messages and agent were set
            assert mock_session.messages == []
            assert mock_session.agent is None
    
    def test_display_message(self):
        """Test message display function."""
        from src.ui.chat_interface import display_message
        
        message = {
            "role": "user",
            "content": "What is the current generation?"
        }
        
        with patch.object(st, 'chat_message') as mock_chat, \
             patch.object(st, 'write') as mock_write:
            
            mock_context = MagicMock()
            mock_chat.return_value.__enter__.return_value = mock_context
            
            display_message(message)
            
            mock_chat.assert_called_once_with("user")
    
    def test_process_user_input(self):
        """Test processing user input."""
        from src.ui.chat_interface import process_user_input
        
        # Create mock session state with mock list
        mock_session = MagicMock()
        mock_messages = MagicMock()
        mock_session.messages = mock_messages
        mock_session.agent = Mock()
        
        with patch.object(st, 'session_state', mock_session), \
             patch('src.ui.chat_interface.process_with_loading', return_value="Current generation is 5000 MW"):
                
                result = process_user_input("What is the current generation?")
                
                # Check that append was called twice
                assert mock_messages.append.call_count == 2
                
                # Check the calls
                calls = mock_messages.append.call_args_list
                assert calls[0][0][0]['role'] == 'user'
                assert calls[1][0][0]['role'] == 'assistant'
    
    def test_error_display(self):
        """Test error message display."""
        from src.ui.chat_interface import display_error
        
        with patch.object(st, 'error') as mock_error:
            display_error("Connection failed")
            
            mock_error.assert_called_once_with("Error: Connection failed")
    
    def test_loading_state(self):
        """Test loading state during API calls."""
        from src.ui.chat_interface import process_with_loading
        
        async def mock_api_call():
            return "API Response"
        
        with patch.object(st, 'spinner') as mock_spinner:
            mock_context = MagicMock()
            mock_spinner.return_value.__enter__.return_value = mock_context
            
            result = process_with_loading(mock_api_call, "Fetching data...")
            
            mock_spinner.assert_called_once_with("Fetching data...")
    
    def test_chat_history_persistence(self):
        """Test chat history is maintained in session."""
        from src.ui.chat_interface import add_to_history
        
        # Create mock session state with mock messages list
        mock_session = MagicMock()
        mock_messages = MagicMock()
        mock_session.messages = mock_messages
        
        with patch.object(st, 'session_state', mock_session):
            add_to_history("user", "First message")
            add_to_history("assistant", "First response") 
            add_to_history("user", "Second message")
            
            # Check that append was called 3 times
            assert mock_messages.append.call_count == 3
            
            # Check the content of the calls
            calls = mock_messages.append.call_args_list
            assert calls[0][0][0]['content'] == "First message"
            assert calls[0][0][0]['role'] == "user"
            assert calls[2][0][0]['role'] == "user"