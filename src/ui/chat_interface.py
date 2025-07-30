"""Streamlit chat interface for the electricity chatbot."""
import streamlit as st
import asyncio
from typing import Dict, Any, List
from agents.mock_electricity_agent import create_mock_electricity_agent as create_electricity_agent


def initialize_chat():
    """Initialize chat interface and session state."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'agent' not in st.session_state:
        st.session_state.agent = None


def display_message(message: Dict[str, str]):
    """Display a chat message."""
    with st.chat_message(message["role"]):
        st.write(message["content"])


def add_to_history(role: str, content: str):
    """Add message to chat history."""
    st.session_state.messages.append({"role": role, "content": content})


def display_error(error_message: str):
    """Display error message."""
    st.error(f"Error: {error_message}")


async def get_agent_response(question: str) -> str:
    """Get response from the electricity agent."""
    if st.session_state.agent is None:
        st.session_state.agent = await create_electricity_agent()
    
    return await st.session_state.agent.query(question)


def process_with_loading(async_func, loading_text: str = "Processing..."):
    """Process async function with loading spinner."""
    with st.spinner(loading_text):
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(async_func())
            return result
        finally:
            loop.close()


def process_user_input(user_input: str) -> str:
    """Process user input and get agent response."""
    # Add user message to history
    add_to_history("user", user_input)
    
    # Get agent response
    response = process_with_loading(
        lambda: get_agent_response(user_input),
        "Getting electricity data..."
    )
    
    # Add assistant response to history
    add_to_history("assistant", response)
    
    return response


def render_chat_interface():
    """Render the main chat interface."""
    st.title("🔌 NZ Electricity Data Chatbot")
    st.markdown("Ask me questions about New Zealand's electricity generation, pricing, and emissions!")
    
    # Initialize chat
    initialize_chat()
    
    # Display chat history
    for message in st.session_state.messages:
        display_message(message)
    
    # Chat input
    if prompt := st.chat_input("Ask about NZ electricity data..."):
        # Display user message immediately
        display_message({"role": "user", "content": prompt})
        
        try:
            # Process and get response
            response = process_user_input(prompt)
            
            # Display assistant response
            display_message({"role": "assistant", "content": response})
            
        except Exception as e:
            error_msg = "Sorry, I encountered an error processing your request. Please try again."
            display_error(error_msg)
            add_to_history("assistant", error_msg)


def render_sidebar():
    """Render sidebar with example queries and info."""
    with st.sidebar:
        st.header("💡 Example Questions")
        
        example_questions = [
            "What is the current power generation in NZ?",
            "Show me the spot prices by region",
            "What percentage of energy is renewable?",
            "What's the carbon intensity right now?",
            "Compare hydro vs wind generation",
            "How much solar power is being generated?"
        ]
        
        for question in example_questions:
            if st.button(question, key=f"example_{hash(question)}"):
                # Add to chat when clicked
                st.session_state.messages.append({"role": "user", "content": question})
                try:
                    response = process_user_input(question)
                except Exception as e:
                    error_msg = "Error processing example question. Please try again."
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.rerun()
        
        st.divider()
        
        st.markdown("""
        ### About
        This chatbot uses:
        - **Strands Agents** framework
        - **Claude Sonnet 4.0** for AI responses
        - **Real-time NZ electricity APIs**
        
        ### Data Sources
        - em6 API (generation data)
        - EMI API (market data)
        - Transpower (system data)
        """)


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="NZ Electricity Chatbot",
        page_icon="⚡",
        layout="wide"
    )
    
    # Render sidebar
    render_sidebar()
    
    # Render main chat interface
    render_chat_interface()


if __name__ == "__main__":
    main()