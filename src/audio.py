import io
import wave
import struct
import math
import pygame


class RetroAudio:
    """
    Sintetizador procedural de efectos de sonido estilo NES 8-bit.
    Genera ondas de audio auténticas en memoria sin requerir descargar archivos externos.
    """

    def __init__(self):
        self.enabled = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.enabled = True
        except Exception:
            self.enabled = False

        self.sounds = {}
        if self.enabled:
            self._generate_all_sounds()

    def _create_wav_sound(self, sample_rate: int, samples: list) -> pygame.mixer.Sound:
        """Convierte una lista de muestras de audio en un objeto Sound de Pygame."""
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            raw_data = struct.pack("<" + "h" * len(samples), *samples)
            wav.writeframes(raw_data)
        buf.seek(0)
        return pygame.mixer.Sound(buf)

    def _generate_all_sounds(self):
        sr = 22050

        # 1. Salto (Frecuencia ascendente rápida de 180Hz a 450Hz)
        jump_samples = []
        duration = 0.15
        total_samples = int(sr * duration)
        for i in range(total_samples):
            t = i / total_samples
            freq = 180 + 280 * t
            val = 14000 * (1 if math.sin(2 * math.pi * freq * (i / sr)) > 0 else -1)
            val = int(val * (1.0 - t * 0.7))
            jump_samples.append(val)
        self.sounds["jump"] = self._create_wav_sound(sr, jump_samples)

        # 2. Moneda (Doble tono agudo: B5 a E6)
        coin_samples = []
        part1 = int(sr * 0.08)
        part2 = int(sr * 0.28)
        for i in range(part1):
            val = 15000 * (1 if math.sin(2 * math.pi * 987.77 * (i / sr)) > 0 else -1)
            coin_samples.append(int(val))
        for i in range(part2):
            decay = 1.0 - (i / part2)
            val = 16000 * (1 if math.sin(2 * math.pi * 1318.51 * (i / sr)) > 0 else -1)
            coin_samples.append(int(val * decay))
        self.sounds["coin"] = self._create_wav_sound(sr, coin_samples)

        # 3. Pisotón (Stomp / Golpe sordo)
        stomp_samples = []
        duration = 0.12
        total_samples = int(sr * duration)
        for i in range(total_samples):
            t = i / total_samples
            freq = 160 * (1.0 - t * 0.6)
            val = int(18000 * math.sin(2 * math.pi * freq * (i / sr)) * (1.0 - t))
            stomp_samples.append(val)
        self.sounds["stomp"] = self._create_wav_sound(sr, stomp_samples)

        # 4. Champiñón / Power-up (Arpegio ascendente)
        powerup_samples = []
        freqs = [330, 392, 659, 523, 587, 784]
        samples_per_note = int(sr * 0.07)
        for freq in freqs:
            for i in range(samples_per_note):
                val = 14000 * (1 if math.sin(2 * math.pi * freq * (i / sr)) > 0 else -1)
                powerup_samples.append(int(val))
        self.sounds["powerup"] = self._create_wav_sound(sr, powerup_samples)

        # 5. Destrucción de ladrillo (Ruido crujiente)
        brick_samples = []
        duration = 0.16
        total = int(sr * duration)
        import random
        for i in range(total):
            decay = 1.0 - (i / total)
            val = int(random.uniform(-16000, 16000) * decay)
            brick_samples.append(val)
        self.sounds["brick"] = self._create_wav_sound(sr, brick_samples)

        # 6. Disparo de Bola de Fuego
        fire_samples = []
        duration = 0.1
        total = int(sr * duration)
        for i in range(total):
            t = i / total
            freq = 800 - 500 * t
            val = int(12000 * math.sin(2 * math.pi * freq * (i / sr)) * (1.0 - t))
            fire_samples.append(val)
        self.sounds["fireball"] = self._create_wav_sound(sr, fire_samples)

        # 7. Asta de bandera (Fanfarria de victoria)
        victory_samples = []
        fanfare = [440, 554, 659, 880]
        for note in fanfare:
            for i in range(int(sr * 0.14)):
                decay = 1.0 - (i / (sr * 0.14)) * 0.4
                val = int(14000 * (1 if math.sin(2 * math.pi * note * (i / sr)) > 0 else -1) * decay)
                victory_samples.append(val)
        self.sounds["flagpole"] = self._create_wav_sound(sr, victory_samples)

    def play(self, sound_name: str):
        """Reproduce un efecto de sonido por nombre."""
        if self.enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception:
                pass


# Instancia única global
audio = RetroAudio()
