import pygame

pygame.mixer.init()

# Use raw strings for Windows paths
correct_sound = pygame.mixer.Sound(r"D:\project\sound\sonido-correcto-331225.wav")
wrong_sound = pygame.mixer.Sound(r"D:\project\sound\buzzer-or-wrong-answer-20582.wav")
times_up_sound = pygame.mixer.Sound(r"D:\project\sound\ticking-clock-sound-effect-1-mp3-edition-264451.wav")
button_click_sound = pygame.mixer.Sound(r"D:\project\sound\ui-click-43196.wav")

def play_correct():
    correct_sound.play()

def play_wrong():
    wrong_sound.play()

def play_time_up():
    times_up_sound.play()

def play_button_click():
    button_click_sound.play()
