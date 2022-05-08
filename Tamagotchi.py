import time
feed_increment = 30
clean_increment = 30
happy_increment = 30
startVal = 100

class Tamagotchi():
    def __init__(self, name):
        self.name = name
        self.hunger = startVal
        self.happy = startVal
        self.age = 0
        self.hygiene = startVal
        self.birthTime = time.time()
        self.timeFed = time.time()
        self.timePet = time.time()
        self.timeClean = time.time()
        self.state = 'Alive'
        self.image = r'.\cogs\images\Baby.png'

    def update(self, name, age, birthTime, hunger, happy, hygiene, image, timeFed, timePet, timeClean, state):
        self.name = name
        self.hunger = hunger
        self.happy = happy
        self.age = age
        self.hygiene = hygiene
        self.birthTime = birthTime
        self.timeFed = timeFed
        self.timePet = timePet
        self.timeClean = timeClean
        self.image = image
        self.state = state

#we could implement it so that the values are a multiple of 10 so we dont have to worry about it being b/n 90-100
    def feed(self):
        self.timeFed = time.time()
        self.hunger += feed_increment
        if self.hunger > startVal:
            self.hunger = startVal

    def clean(self):
        self.timeClean = time.time()
        self.hygiene += clean_increment
        if self.hygiene > startVal:
            self.hygiene = startVal

    def play(self):
        self.timePet = time.time()
        self.happy += happy_increment
        if self.happy > startVal:
            self.happy = startVal

    def picStatus(self):
        if (self.age >= 1):
            if (self.hygiene < 50 and self.hygiene <= self.happy and self.hygiene <= self.hunger):
                self.image = r'.\cogs\images\dirty.png'
            elif (self.hunger <= 50):
                self.image = r'.\cogs\images\Hungry.png'
            elif (self.happy <= 50):
                self.image = r'.\cogs\images\sad.png'
            else:
                self.image = r'.\cogs\images\Happy.png'

        if (self.state == 'Dead'):
            self.image = r'.\cogs\images\Dead.png'
        elif (self.state == 'Away'):
            self.image = r'.\cogs\images\Fled.png'
        elif (self.state == 'Sick'):
            self.image = r'.\cogs\images\Sick.png'

