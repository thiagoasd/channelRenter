class Rent:
    def __init__(self, name, voice, text, role, owner, secret=False):
        self.name = name
        self.voice = voice
        self.text = text
        self.role = role
        self.owner = owner
        self.secret = secret
