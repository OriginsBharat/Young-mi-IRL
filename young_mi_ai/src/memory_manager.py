import sqlite3
import logging
from datetime import datetime

class MemoryManager:
    def __init__(self, config):
        self.db_path = config.get('database_file', 'memory.db')
        self._create_database()

    def _get_connection(self):
        """Creates a connection to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def _create_database(self):
        """Creates the memories table if it doesn't already exist."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS memories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        memory_text TEXT NOT NULL,
                        timestamp DATETIME NOT NULL
                    )
                """)
                conn.commit()
                logging.info(f"Database '{self.db_path}' initialized and table 'memories' is ready.")
        except sqlite3.Error as e:
            logging.error(f"Database error while creating table: {e}")

    def save_memory(self, user_id, memory_text):
        """Saves a new memory to the database."""
        if not memory_text or not isinstance(memory_text, str) or len(memory_text) < 5:
            logging.warning(f"Attempted to save a trivial or invalid memory: {memory_text}")
            return

        timestamp = datetime.utcnow()
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO memories (user_id, memory_text, timestamp) VALUES (?, ?, ?)",
                    (user_id, memory_text, timestamp)
                )
                conn.commit()
                logging.info(f"Saved memory for user {user_id}: {memory_text}")
        except sqlite3.Error as e:
            logging.error(f"Failed to save memory for user {user_id}: {e}")

    def get_recent_memories(self, user_id, limit=10):
        """Retrieves the most recent memories for a user."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT memory_text FROM memories WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
                    (user_id, limit)
                )
                memories = [row[0] for row in cursor.fetchall()]
                logging.info(f"Retrieved {len(memories)} memories for user {user_id}.")
                return memories
        except sqlite3.Error as e:
            logging.error(f"Failed to retrieve memories for user {user_id}: {e}")
            return []

    def format_memories_for_prompt(self, user_id, limit=10):
        """Formats memories into a string suitable for an AI prompt."""
        memories = self.get_recent_memories(user_id, limit)
        if not memories:
            return "No recent memories."

        formatted_string = "\n".join(f"- {mem}" for mem in memories)
        return f"Here are some recent memories we share:\n{formatted_string}"