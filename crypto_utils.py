import os
import secrets
import string
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
def hash_master_password(password):
    salt = os.urandom(32)
    key = derive_key(password, salt)
    return key, salt
def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000
    )
    return kdf.derive(password.encode("utf-8"))
def verify_master_password(password, stored_hash, salt):
    try:
        candidate = derive_key(password, bytes(salt))
        return secrets.compare_digest(candidate, bytes(stored_hash))
    except Exception:
        return False
def encrypt_password(plain_text, key):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    encrypted = aesgcm.encrypt(nonce, plain_text.encode("utf-8"), None)
    return nonce + encrypted
def decrypt_password(blob, key):
    blob = bytes(blob)
    nonce = blob[:12]
    encrypted = blob[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, encrypted, None).decode("utf-8")
def generate_password(length=20, use_upper=True, use_lower=True,
                      use_digits=True, use_symbols=True, exclude_ambiguous=False):
    pool = ""
    required = []
    if use_upper:
        chars = string.ascii_uppercase
        if exclude_ambiguous:
            chars = chars.replace("I", "").replace("O", "")
        pool += chars
        required.append(secrets.choice(chars))
    if use_lower:
        chars = string.ascii_lowercase
        if exclude_ambiguous:
            chars = chars.replace("l", "").replace("o", "").replace("i", "")
        pool += chars
        required.append(secrets.choice(chars))
    if use_digits:
        chars = string.digits
        if exclude_ambiguous:
            chars = chars.replace("0", "").replace("1", "")
        pool += chars
        required.append(secrets.choice(chars))
    if use_symbols:
        chars = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        pool += chars
        required.append(secrets.choice(chars))
    if not pool:
        pool = string.ascii_letters + string.digits
    extra = [secrets.choice(pool) for _ in range(length - len(required))]
    all_chars = required + extra
    for i in range(len(all_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        all_chars[i], all_chars[j] = all_chars[j], all_chars[i]
    return "".join(all_chars)
def password_strength(password):
    score = 0
    length = len(password)
    if length >= 8:  score += 10
    if length >= 12: score += 15
    if length >= 16: score += 15
    if length >= 20: score += 10
    if any(c.isupper() for c in password):  score += 10
    if any(c.islower() for c in password):  score += 10
    if any(c.isdigit() for c in password):  score += 10
    if any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password): score += 15
    if len(set(password)) < length * 0.5:
        score -= 20
    score = max(0, min(score, 100))
    if score < 30:   label = "Weak"
    elif score < 55: label = "Fair"
    elif score < 80: label = "Strong"
    else:            label = "Very Strong"
    return score, label
