
class Password:

    def __init__(self,site,cipher_pass):
        self.site = site
        self.cipher_pass = cipher_pass
    
    def get_pass(self):
        return self.cipher_pass