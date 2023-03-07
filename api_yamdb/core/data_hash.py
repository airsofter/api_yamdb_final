"""Методы """
import hashlib


def hash_sha254(data):
    """Метод для хеширования данных по алгоритму SHA254."""
    return hashlib.sha256(str(data).encode()).hexdigest()
