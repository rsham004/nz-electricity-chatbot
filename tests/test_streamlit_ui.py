import pytest
from unittest.mock import Mock, patch, MagicMock
import streamlit as st

# Tests for Streamlit UI components


class TestStreamlitUI:
    """Test Streamlit chat interface."""
    
    def test_chat_interface_initialization(self):
        """Test chat interface initializes correctly."""
        from src.ui.chat_interface import initialize_chat
        
        with patch.object(st, 'session_state', {}):
            initialize_chat()
            
            assert 'messages' in st.session_state
            assert 'agent' in st.session_state
            assert isinstance(st.session_state.messages, list)
    
    def test_display_message(self):
        """Test message display function."""
        from src.ui.chat_interface import display_message
        
        message = {
            "role": "user",
            "content": "What is the current generation?"
        }
        
        with patch.object(st, 'chat_message') as mock_chat:
            mock_context = MagicMock()
            mock_chat.return_value.__enter__.return_value = mock_context
            
            display_message(message)
            
            mock_chat.assert_called_once_with("user")
            mock_context.write.assert_called_once_with("What is the current generation?")
    
    def test_process_user_input(self):
        """Test processing user input."""
        from src.ui.chat_interface import process_user_input
        
        with patch.object(st, 'session_state', {'messages': [], 'agent': Mock()}):
            with patch('src.ui.chat_interface.get_agent_response', return_value="Current generation is 5000 MW"):
                
                result = process_user_input("What is the current generation?")
                
                assert len(st.session_state.messages) == 2
                assert st.session_state.messages[0]['role'] == 'user'
                assert st.session_state.messages[1]['role'] == 'assistant'
                assert "5000 MW" in st.session_state.messages[1]['content']
    
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
        
        with patch.object(st, 'session_state', {'messages': []}):
            add_to_history("user", "First message")
            add_to_history("assistant", "First response")
            add_to_history("user", "Second message")
            
            assert len(st.session_state.messages) == 3
            assert st.session_state.messages[0]['content'] == "First message"
            assert st.session_state.messages[2]['role'] == "user"