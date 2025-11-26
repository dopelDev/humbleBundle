import unittest
from hashlib import sha256

from api.security import hash_password, is_sha256_hash, verify_password


class SecurityUtilsTests(unittest.TestCase):
    def test_is_sha256_hash(self):
        digest = sha256(b'example').hexdigest()
        self.assertTrue(is_sha256_hash(digest))
        self.assertFalse(is_sha256_hash('not-a-hash'))

    def test_hash_password_accepts_sha256_input(self):
        digest = sha256(b'shared-secret').hexdigest()
        hashed = hash_password(digest)
        self.assertTrue(verify_password(digest, hashed))

    def test_hash_password_accepts_plain_input(self):
        plain = 'PlainPassword123'
        hashed = hash_password(plain)
        self.assertTrue(verify_password(plain, hashed))


if __name__ == '__main__':
    unittest.main()

