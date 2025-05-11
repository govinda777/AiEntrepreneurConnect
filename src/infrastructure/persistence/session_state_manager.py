import streamlit as st
from typing import Any, Optional
from ...application.interfaces.i_state_manager import IStateManager

class SessionStateManager(IStateManager):
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from Streamlit's session state."""
        return st.session_state.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in Streamlit's session state."""
        st.session_state[key] = value
    
    def delete(self, key: str) -> None:
        """Delete a value from Streamlit's session state."""
        if key in st.session_state:
            del st.session_state[key]
    
    def clear(self) -> None:
        """Clear all session state."""
        for key in list(st.session_state.keys()):
            del st.session_state[key] 