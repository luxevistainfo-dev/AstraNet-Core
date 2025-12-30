# snapshot/backup.py

import pickle

def save_snapshot(chain, filename="snapshot.pkl"):
    """
    Направи snapshot на целата мрежа за backup.
    Поддржува или chain објект со .chain атрибут или директно податоци.
    """
    # Ако chain има .chain атрибут, користи го, инаку користи го директно
    data = chain.chain if hasattr(chain, 'chain') else chain
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def load_snapshot(filename="snapshot.pkl"):
    """
    Вчитај snapshot од фајл.
    """
    with open(filename, "rb") as f:
        return pickle.load(f)
