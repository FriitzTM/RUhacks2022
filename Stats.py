import time

import Tamagotchi


def update_stats(pet: Tamagotchi):
    new_time = time.time()
    cal_hygiene(new_time, pet)
    cal_happy(new_time, pet)
    cal_hunger(new_time, pet)
    cal_age(new_time, pet)
    pet.timeSince = new_time
    pet.picStatus()


def cal_hunger(current_time, pet: Tamagotchi):
    time_since = current_time - pet.timeFed
    pet.hunger -= (10 * (time_since // 30))
    if pet.hunger <= 0:
        pet.hunger = 0
        pet.state = 'Dead'
    return


def cal_hygiene(current_time, pet: Tamagotchi):
    time_since = current_time - pet.timeClean
    pet.hygiene -= (10 * (int(time_since / 45)))
    if pet.hygiene <= 0:
        pet.hygiene = 0
        pet.state = 'Sick'
    return


def cal_happy(current_time, pet: Tamagotchi):
    time_since = current_time - pet.timePet
    pet.happy -= (10 * (int(time_since / 60)))
    if pet.happy <= 0:
        pet.happy = 0
        pet.state = 'Away'
    return


def cal_age(current_time, pet: Tamagotchi):
    time_since = current_time - pet.birthTime
    pet.age = (int(time_since / 70))
    return
