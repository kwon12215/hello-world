import pygame


class SoundManager:
    def sound_play(self, sound):
        pygame.mixer.init()
        Sound = pygame.mixer.Sound(sound)
        Sound.play(0)

    def WinSound(self):
        self.sound_play('Sound/WinSound.ogg')

    def LoseSound(self):
        self.sound_play('Sound/LoseSound.ogg')

    def SetStonSound(self):
        self.sound_play('Sound/ChakSu.ogg')

    def ButtonClickSound(self):
        self.sound_play('Sound/Enter.ogg')


if __name__ == '__main__':
    sound_manager = SoundManager()
    sound_manager.ButtonClickSound()
