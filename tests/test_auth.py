import tempfile
import unittest
from pathlib import Path

from app.database import SignalStore
from app.services.auth import (
    hash_password,
    hash_session_token,
    new_session,
    public_user,
    verify_password,
)


class AuthTest(unittest.TestCase):
    def test_password_hash_is_salted_and_verifiable(self):
        first = hash_password("long-password")
        second = hash_password("long-password")

        self.assertNotEqual(first, second)
        self.assertTrue(verify_password("long-password", first))
        self.assertFalse(verify_password("wrong-password", first))

    def test_user_session_and_feature_permissions_are_persisted(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            user = store.create_user(
                username="viewer",
                password_hash=hash_password("viewer-password"),
                role="user",
                features=["overview", "positions"],
            )
            token, token_hash, expires_at = new_session(30)
            store.create_session(
                token_hash=token_hash,
                user_id=user["id"],
                expires_at=expires_at,
            )

            session_user = store.get_session_user(hash_session_token(token))

            self.assertEqual(session_user["username"], "viewer")
            self.assertEqual(session_user["features"], ["overview", "positions"])
            self.assertEqual(public_user(session_user)["role"], "user")

    def test_disabling_user_invalidates_session(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            user = store.create_user(
                username="viewer",
                password_hash=hash_password("viewer-password"),
                role="user",
                features=["overview"],
            )
            _, token_hash, expires_at = new_session(30)
            store.create_session(
                token_hash=token_hash,
                user_id=user["id"],
                expires_at=expires_at,
            )

            store.update_user(user["id"], active=False)

            self.assertIsNone(store.get_session_user(token_hash))

    def test_changing_password_invalidates_session(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = SignalStore(Path(temp_dir) / "signals.db")
            user = store.create_user(
                username="admin",
                password_hash=hash_password("old-password"),
                role="admin",
                features=[],
            )
            _, token_hash, expires_at = new_session(30)
            store.create_session(
                token_hash=token_hash,
                user_id=user["id"],
                expires_at=expires_at,
            )

            store.update_user(
                user["id"],
                password_hash=hash_password("new-password"),
            )

            self.assertIsNone(store.get_session_user(token_hash))


if __name__ == "__main__":
    unittest.main()
