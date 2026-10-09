# Setting Up STT — SpeechRecognition + Microphone

The first real step of the chained agent: get the user's spoken audio
converted into text. One package, four calls.

---

## 🟢 Beginner — the package, and the four-step shape

```bash
pip install SpeechRecognition
```

```python
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
```


| Call                                | Does                                                            |
| ----------------------------------- | --------------------------------------------------------------- |
| `sr.Recognizer()`                   | the object that does the actual speech-to-text work             |
| `sr.Microphone()` as a `with` block | opens the system mic as the audio source                        |
| `.adjust_for_ambient_noise(source)` | calibrates to cut background noise                              |
| `.listen(source)`                   | records until a ~2 second pause, then stops                     |
| `.recognize_google(audio)`          | sends the recorded audio to a backend, returns transcribed text |


---



## 🟡 Intermediate — `recognize_google` is one of several backends

`.recognize_google(...)` is just one STT provider the package supports -
the library offers several. Swapping providers later is a one-line
change, not a rewrite of the mic-handling code around it.

---



## 🔴 Expert — the macOS gotcha that will happen

```text
pip install SpeechRecognition
                |
                v
     python main.py  ->  "could not find PyAudio, check installation"
```

`pip install SpeechRecognition` alone doesn't give microphone access -
that needs **PyAudio**, which wraps the C library **PortAudio**. On macOS,
PyAudio can't build without PortAudio already present on the system:

```bash
brew install portaudio                  # the system library PyAudio links against
pip install SpeechRecognition[audio]    # (or: pip install pyaudio)
```

**The order matters** - install `portaudio` first. This is a documented,
expected error, not a sign anything is wrong with the code.

---



## Quick recap


| Term                       | One-line definition                                                                                      |
| -------------------------- | -------------------------------------------------------------------------------------------------------- |
| **SpeechRecognition**      | the Python package providing STT, with multiple backend providers                                        |
| **PyAudio / PortAudio**    | the microphone-access layer SpeechRecognition depends on - needs `brew install portaudio` first on macOS |
| `adjust_for_ambient_noise` | calibrates for background noise before listening                                                         |
| `listen(source)`           | records until the user pauses, then returns the audio                                                    |


