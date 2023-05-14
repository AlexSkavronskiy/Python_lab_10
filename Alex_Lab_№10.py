import json
import requests
import pyttsx3, pyaudio, vosk

tts = pyttsx3.init('sapi5')

voices = tts.getProperty('voices')
tts.setProperty('voices', 'en')

for voice in voices:
    if voice.name == 'Microsoft Zira Desktop - English (United States)':
        tts.setProperty('voice', voice.id)

model = vosk.Model('vosk-model-small-en-us-0.15')
record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 input=True,
                 frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']


def speak(say):
    tts.say(say)
    tts.runAndWait()


def find_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[0]
    else:
        speak('Error while getting data')
        return None


speak('start')

for text in listen():

    if text == 'goodbye':
        speak('Goodbye!')
        break

    elif text == 'hello':
        speak("Hello! How can I help you?")

    elif 'find' in text:
        new_word = text.split()
        find = find_word(f'{new_word[len(new_word) - 1]}')
        print(find)

    elif 'phonetic' in text:
        new_word = text.split()
        find = find_word(f'{new_word[len(new_word) - 1]}')
        phonetic = find['phonetic']
        print(phonetic)

    elif 'meaning' in text:
        new_word = text.split()
        find = find_word(f"{new_word[len(new_word) - 1]}")
        meaning = find['meanings']
        print(meaning)
