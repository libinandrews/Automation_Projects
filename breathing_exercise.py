import os
import time
import threading
import pygame
from gtts import gTTS
from abc import ABC, abstractmethod


OUTPUT_FOLDER = "output/breathexercise"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)  # Ensure directory exists


class TextToSpeech(ABC):
    """Abstract base class for text-to-speech conversion."""

    @abstractmethod
    def speak(self, text: str) -> float:
        pass

    @abstractmethod
    def speak_async(self, text: str) -> float:
        pass


class GTTSpeech(TextToSpeech):
    """
    Implementation of TextToSpeech using gTTS and pygame.
    - Uses offline MP3 caching for repeated phrases.
    """

    def __init__(self) -> None:
        pygame.mixer.init()

    def _get_audio_path(self, text: str) -> str:
        """Generate a consistent filename based on the text content."""
        sanitized_text = "".join(c if c.isalnum() or c.isspace() else "_" for c in text)
        filename = f"{sanitized_text[:50]}.mp3"  # Trim long names
        return os.path.join(OUTPUT_FOLDER, filename)

    def _generate_audio(self, text: str) -> str:
        """Generate and save an audio file for offline use."""
        audio_path = self._get_audio_path(text)
        if not os.path.exists(audio_path):
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(audio_path)
        return audio_path

    def _estimate_speech_duration(self, text: str) -> float:
        """Estimate duration of spoken text."""
        words = len(text.split())
        chars = len(text)
        return (words * 0.3) + (chars * 0.02)

    def speak(self, text: str) -> float:
        """Synchronously speak text, using cached audio if available."""
        audio_path = self._generate_audio(text)
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        return self._estimate_speech_duration(text)

    def speak_async(self, text: str) -> float:
        """Asynchronously speak text, using cached audio."""
        thread = threading.Thread(target=self.speak, args=(text,))
        thread.start()
        return self._estimate_speech_duration(text)


class CountdownTimer(threading.Thread):
    """Threaded countdown timer that speaks countdown numbers asynchronously."""

    def __init__(self, duration: int, tts: GTTSpeech) -> None:
        super().__init__()
        self.duration = int(duration)
        self.tts = tts
        self._stop_event = threading.Event()

    def run(self) -> None:
        for i in range(self.duration, 0, -1):
            if self._stop_event.is_set():
                break
            self.tts.speak_async(str(i))
            time.sleep(1)

    def stop(self) -> None:
        self._stop_event.set()


class BreathingExercise:
    """
    Guides the user through a structured breathing exercise using the 4-7-8 technique:
      - Inhale for 4 seconds
      - Hold for 7 seconds
      - Exhale for 8 seconds
    """

    def __init__(self, tts: TextToSpeech) -> None:
        self.tts = tts

    def breath_phase(self, instruction: str, duration: int) -> None:
        """
        Speaks the instruction and concurrently starts a countdown for the adjusted duration.
        """
        speech_duration = self.tts.speak(instruction)
        adjusted_sleep_time = max(0, duration - speech_duration)

        countdown = CountdownTimer(adjusted_sleep_time, self.tts)
        countdown.start()
        time.sleep(adjusted_sleep_time)
        countdown.stop()
        countdown.join()

    def breath_cycle(self, inhale: int, hold: int, exhale: int) -> None:
        """
        Executes one complete breathing cycle.
        """
        self.breath_phase(
            f"Inhale slowly for {inhale} seconds, expanding your lungs fully.", inhale
        )
        self.breath_phase(
            f"Hold your breath for {hold} seconds to let the oxygen circulate.", hold
        )
        self.breath_phase(
            f"Exhale slowly for {exhale} seconds, releasing all tension.", exhale
        )

    def start_exercise(
        self, total_duration: int = 300, inhale: int = 4, hold: int = 7, exhale: int = 8
    ) -> None:
        """
        Start the guided breathing exercise for the specified total duration.
        Default total_duration is 300 seconds (5 minutes). Adjust as needed.
        """
        self.tts.speak(
            "Welcome to your guided breathing exercise. Sit comfortably with your back straight and relax your shoulders."
        )
        time.sleep(2)
        self.tts.speak(
            "We will use the 4-7-8 breathing technique, known to reduce stress and promote relaxation."
        )
        time.sleep(2)

        start_time = time.time()
        cycles_completed = 0

        while time.time() - start_time < total_duration:
            self.breath_cycle(inhale, hold, exhale)
            cycles_completed += 1

        self.tts.speak(
            f"Exercise completed! You completed {cycles_completed} cycles. Enjoy the calm and relaxation that follows."
        )


if __name__ == '__main__':
    # Default total exercise duration is 5 minutes (300 seconds)
    tts_engine = GTTSpeech()
    breathing_session = BreathingExercise(tts_engine)
    breathing_session.start_exercise(total_duration=300)
