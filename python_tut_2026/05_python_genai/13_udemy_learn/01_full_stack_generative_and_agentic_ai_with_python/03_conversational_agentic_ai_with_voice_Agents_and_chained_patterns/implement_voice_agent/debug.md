## PyAudio fix on macOS (speech_recognition)

| # | Step | Command | Why | Result |
|---|---|---|---|---|
| 1 | Check for PortAudio | `brew list --versions portaudio` | PyAudio only binds to this C library; pip has nothing to compile against without it. | portaudio NOT installed |
| 2 | Install PortAudio | `brew install portaudio` | The native audio layer. Homebrew ships a prebuilt arm64 bottle, so no compiler is involved here. | portaudio 19.7.0 |
| 3 | Install PyAudio into the active venv | `pip install pyaudio` | Builds the binding against step 2. It must go into the same venv that runs main.py (the repo-root .venv in the traceback). | built pyaudio 0.2.14 |
| 4 | Verify the exact call that crashed | `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names()); sr.Microphone()"` | Proves Microphone() now initialises and shows which input devices PortAudio can see. | [1] MacBook Air Microphone |
| 5 | Run the script | `python main.py` | Speak after “Speak something…”, pause about 2 s. recognize_google sends the clip to Google's free web STT (internet needed, no key). | You said: … |
