import sqlite3
from .UserSettings import UserSettings 
class Database:
    def __init__(self, db_name="settings.db"):
        """Initialize the database and create the settings table."""
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        """Create the user_settings table if it doesn't already exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                id INTEGER PRIMARY KEY,
                cpu_threshold INTEGER DEFAULT 80,
                memory_threshold INTEGER DEFAULT 80,
                disk_threshold INTEGER DEFAULT 80,
                network_threshold INTEGER DEFAULT 1000000,
                gpu_threshold INTEGER DEFAULT 80,
                check_interval INTEGER DEFAULT 10,
                theme TEXT DEFAULT 'Catpuccin'
            )
        """)
        self.connection.commit()

        # Ensure a default entry exists if the table is empty
        self.cursor.execute("SELECT COUNT(*) FROM user_settings")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("""
                INSERT INTO user_settings (cpu_threshold, memory_threshold, disk_threshold, network_threshold, gpu_threshold, check_interval, theme)
                VALUES (80, 80, 80, 1000000, 80, 10, 'Catpuccin')
            """)
            self.connection.commit()

    def get_thresholds(self) -> UserSettings:
        """Retrieve current settings from the database."""
        self.cursor.execute("SELECT * FROM user_settings WHERE id = 1")
        result = self.cursor.fetchone()
        if result:
            return UserSettings(
                cpu_threshold=result[1],
                memory_threshold=result[2],
                disk_threshold=result[3],
                network_threshold=result[4],
                gpu_threshold=result[5],
                check_interval=result[6],
                theme=result[7]
            )
        return None

    def update_thresholds(self, settings: UserSettings):
        """Update user settings in the database using a UserSettings instance."""
        self.cursor.execute("""
            INSERT OR REPLACE INTO user_settings (id, cpu_threshold, memory_threshold, disk_threshold, network_threshold, gpu_threshold, check_interval, theme)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?)
        """, (
            settings.cpu_threshold,
            settings.memory_threshold,
            settings.disk_threshold,
            settings.network_threshold,
            settings.gpu_threshold,
            settings.check_interval,
            settings.theme
        ))
        self.connection.commit()

    def update_theme(self, theme):
        """Update the theme setting in the database."""
        self.cursor.execute("UPDATE user_settings SET theme = ?", (theme,))
        self.connection.commit()

    def get_theme(self):
        """Retrieve the current theme."""
        self.cursor.execute("SELECT theme FROM user_settings LIMIT 1")
        row = self.cursor.fetchone()
        return row[0] if row else 'Catpuccin'

    def close(self):
        """Close the database connection."""
        self.connection.close()

    def __enter__(self):
        """Context management support for the database connection."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure the database connection is closed when exiting the context."""
        self.close()
