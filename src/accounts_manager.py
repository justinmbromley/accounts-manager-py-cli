from typing import List
from typing import Optional
from datetime import datetime
import sqlite3
import json

from constants import TABLE_NAME
from src.account import Account

class AccountsManager:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def am_add_account(self, account_name: str, account_details: List[str]):
        cursor = self._conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_name TEXT,
                account_details TEXT,
                account_time_last_edited TIMESTAMP
            )
        ''')
        
        account_time_last_edited = datetime.now()
        account_details_json = json.dumps(account_details)

        cursor.execute(f'''
            INSERT INTO {TABLE_NAME} (account_name, account_details, account_time_last_edited)
            VALUES (?, ?, ?)
        ''', (account_name, account_details_json, account_time_last_edited))
        
        self._conn.commit()

    def am_get_account(self, account_id: int) -> Optional[Account]:
        cursor = self._conn.cursor()
        cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE account_id == ?", (account_id,))
        result = cursor.fetchone()

        if result is None:
            return None
        else:
            return Account(result[0], result[1], json.loads(result[2]), result[3])
        
    def am_get_accounts_by_name(self, account_name: str) -> Optional[List[Account]]:
        cursor = self._conn.cursor()
        cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE account_name == ?", (account_name, ))
        result = cursor.fetchall()

        if not result:
            return None
        else:
            accounts = []
            for row in result:
                accounts.append(Account(row[0], row[1], json.loads(row[2]), row[3]))
            return accounts

    def am_get_accounts(self) -> List[Account]:
        cursor = self._conn.cursor()
        cursor.execute(f"SELECT * FROM {TABLE_NAME}")
        result = cursor.fetchall()
        
        accounts = []
        for row in result:
            accounts.append(Account(row[0], row[1], json.loads(row[2]), row[3]))
        return accounts

    def am_update_account_name(self, account_id: int, new_account_name: str):
        cursor = self._conn.cursor()
        cursor.execute(f"UPDATE {TABLE_NAME} SET account_name = ? WHERE account_id = ?", (new_account_name, account_id))
        self._conn.commit()

    def am_update_account_details(self, account_id: int, new_account_details: List[str]):
        cursor = self._conn.cursor()
        cursor.execute(f"UPDATE {TABLE_NAME} SET account_details = ? WHERE account_id = ?", (json.dumps(new_account_details), account_id))
        self._conn.commit()

    def am_delete_account(self, account_id: int):
        cursor = self._conn.cursor()
        cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE account_id = ?", (account_id,))
        self._conn.commit()
