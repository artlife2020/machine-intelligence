# Scalable contract signing pipeline simulation
import hashlib
import json
import time
import uuid

class MemoryStore:
    def __init__(self):
        self.store = {}

    def save(self, key, value):
        self.store[key] = value

    def fetch(self, key):
        return self.store.get(key)

def create_contract(a, b, purpose):
    return {
        "uid": str(uuid.uuid4()),
        "a": a,
        "b": b,
        "purpose": purpose,
        "time": time.time()
    }

def encode(contract):
    return json.dumps(contract, sort_keys=True)

def hash_payload(payload):
    return hashlib.sha256(payload.encode()).hexdigest()

def sign_hash(h, secret):
    return hashlib.sha256(f"{h}:{secret}".encode()).hexdigest()

def verify(h, sig, secret):
    return sign_hash(h, secret) == sig

def pipeline():
    db = MemoryStore()

    contract = create_contract("NodeA", "NodeB", "Inference approval contract")
    encoded = encode(contract)
    h = hash_payload(encoded)

    db.save(h, contract)

    sig = sign_hash(h, "model_key_42")
    valid = verify(h, sig, "model_key_42")

    print("Hash:", h)
    print("Signature:", sig)
    print("Valid:", valid)

    return db, h, sig

def report(db):
    print("\nStored Contracts:")
    for k, v in db.store.items():
        print(k, v)
