import speech_recognition as sr

def main():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)   # noise cancellation
        print("Speak something...")

        audio = r.listen(source)             # blocks until you pause (~2s of silence)
        print("Processing audio...")

        stt = r.recognize_google(audio)      # sends audio to Google's STT backend
        print("You said:", stt)

if __name__ == "__main__":
    main()