# pylint: disable=W0201, E0611

import os
from typing import Any
import uuid

from streamlitapp.utils.chat_utils import save_chat

EMPTY_CHAT_NAME = "Empty chat"
NUM_CHAT_IN_RECENT = 3
DEFAULT_BASE_URL = "http://localhost:8000/"


class SideBar:
    """Manages the sidebar components of the Streamlit application."""

    def __init__(self, st: Any) -> None:
        """
        Initialize the SideBar.

        Args:
            st (Any): The Streamlit object for rendering UI components.
        """
        self.st = st

    def init_side_bar(self) -> None:
        """Initialize and render the sidebar components."""
        with self.st.sidebar:
            self.url_input_field = self.st.text_input(
                label="Service URL",
                value=os.environ.get("SERVICE_URL", DEFAULT_BASE_URL),
            )
            col1, col2, col3 = self.st.columns(3)
            with col1:
                if self.st.button("+ New chat"):
                    if (
                        len(
                            self.st.session_state.user_chats[
                                self.st.session_state["session_id"]
                            ]["messages"]
                        )
                        > 0
                    ):
                        self.st.session_state.run_id = None

                        self.st.session_state["session_id"] = str(uuid.uuid4())
                        self.st.session_state.session_db.get_session(
                            session_id=self.st.session_state["session_id"],
                        )
                        self.st.session_state.user_chats[
                            self.st.session_state["session_id"]
                        ] = {
                            "title": EMPTY_CHAT_NAME,
                            "messages": [],
                        }

            with col2:
                if self.st.button("Delete chat"):
                    self.st.session_state.run_id = None
                    self.st.session_state.session_db.clear()
                    self.st.session_state.user_chats.pop(
                        self.st.session_state["session_id"]
                    )
                    if len(self.st.session_state.user_chats) > 0:
                        chat_id = list(self.st.session_state.user_chats.keys())[0]
                        self.st.session_state["session_id"] = chat_id
                        self.st.session_state.session_db.get_session(
                            session_id=self.st.session_state["session_id"],
                        )
                    else:
                        self.st.session_state["session_id"] = str(uuid.uuid4())
                        self.st.session_state.user_chats[
                            self.st.session_state["session_id"]
                        ] = {
                            "title": EMPTY_CHAT_NAME,
                            "messages": [],
                        }
            with col3:
                if self.st.button("Save chat"):
                    save_chat(self.st)

            self.st.subheader("Recent")  # Style the heading

            all_chats = list(reversed(self.st.session_state.user_chats.items()))
            for chat_id, chat in all_chats[:NUM_CHAT_IN_RECENT]:
                if self.st.button(chat["title"], key=chat_id):
                    self.st.session_state.run_id = None
                    self.st.session_state["session_id"] = chat_id
                    self.st.session_state.session_db.get_session(
                        session_id=self.st.session_state["session_id"],
                    )

            with self.st.expander("Other chats"):
                for chat_id, chat in all_chats[NUM_CHAT_IN_RECENT:]:
                    if self.st.button(chat["title"], key=chat_id):
                        self.st.session_state.run_id = None
                        self.st.session_state["session_id"] = chat_id
                        self.st.session_state.session_db.get_session(
                            session_id=self.st.session_state["session_id"],
                        )

            self.st.divider()
            self.st.header("Upload files from local")
            if "checkbox_state" not in self.st.session_state:
                self.st.session_state.checkbox_state = True

            self.uploaded_files = self.st.file_uploader(
                label="Send files from local",
                accept_multiple_files=True,
                key=f"uploader_images_{self.st.session_state.uploader_key}",
                type=[
                    "png",
                    "jpg",
                    "jpeg",
                    "txt",
                    "docx",
                    "pdf",
                    "rtf",
                    "csv",
                    "tsv",
                    "xlsx",
                ],
            )
