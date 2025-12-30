# snapshot/backup.py

import pickle

def save_snapshot(chain, filename="snapshot.pkl"):
    """
    Направи snapshot на целата мрежа за backup.
    """
    with open(filename, "wb") as f:
        pickle.dump(chain.chain, f)

def load_snapshot(filename="snapshot.pkl"):
    """
    Вчитај snapshot од фајл.
    """
    with open(filename, "rb") as f:
        return pickle.load(f)

