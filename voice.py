import speech_recognition as sr
import pyttsx3

from config import LANGUAGE, VOICE_RATE, VOICE_VOLUME


# =========================================================
# TEXT TO SPEECH
# =========================================================

engine = pyttsx3.init()

engine.setProperty("rate", VOICE_RATE)
engine.setProperty("volume", VOICE_VOLUME)

voices = engine.getProperty("voices")

if voices:
    engine.setProperty("voice", voices[0].id)


def speak(text):
    if not text:
        return

    print(f"JARVIS: {text}")

    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as error:
        print("TTS Error:", error)


# =========================================================
# SPEECH RECOGNITION
# =========================================================

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8


def listen():

    with sr.Microphone() as source:

        print("\nListening...")

        try:

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        except sr.WaitTimeoutError:

            print("No voice detected.")

            return ""

        except Exception as error:

            print("Microphone error:", error)

            return ""

    try:

        print("Recognizing...")

        text = recognizer.recognize_google(
            audio,
            language=LANGUAGE
        )

        print("YOU:", text)

        return text.lower().strip()

    except sr.UnknownValueError:

        print("Could not understand speech.")

        return ""

    except sr.RequestError:

        print("Speech recognition service unavailable.")

        return ""

    except Exception as error:

        print("Recognition error:", error)

        return ""