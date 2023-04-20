class Token():
    def __init__(self, max):
        self.statut = 0
        self.max = max
        self.type = 'Token'

    def __str__(self):
        return self.type + ' : ' + str(self.statut)

    def avancer(self):
        self.statut += 1


class Traque(Token):
    def __init__(self, max = 8):
        super().__init__(max)
        self.type = 'Traque'


class Secour(Token):
    def __init__(self, max = 13):
        super().__init__(max)
        self.type = 'Secour'

if __name__ == '__main__':
    test = Traque()
    print(test)
    test.avancer()
    print(test)