from app import bchain

blockclass=bchain.Blockchain()

def count():
    size=len(blockclass.chain)
    return int(size)
