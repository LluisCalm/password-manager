
class Password:

    def __init__(self,site,cipher_pass):
        self.site = site
        self.cipher_pass = cipher_pass
    
    def get_pass(self):
        return self.cipher_pass
    
    def get_site(self):
        return self.site
    
    def change_pass(self, new_pass):
        self.cipher_pass = new_pass