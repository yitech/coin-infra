from dataclasses

class CryptoRecorder:
    def __init__(self, name: str, server: str, target: str):
        self.name = name
        self.source = server
