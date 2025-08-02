import sqlite3
from pydub import AudioSegment
import os
import json
from vosk import Model, KaldiRecognizer
import wave

# Configura o caminho do ffmpeg e ffprobe explicitamente
from pydub.utils import which
AudioSegment.converter = r"C:\\Users\\LuisaHamon\\Downloads\\ffmpeg-master-latest-win64-gpl-shared\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe"
os.environ["FFMPEG_BINARY"] = AudioSegment.converter
os.environ["FFPROBE_BINARY"] = r"C:\\Users\\LuisaHamon\\Downloads\\ffmpeg-master-latest-win64-gpl-shared\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffprobe.exe"

# Extrai o áudio do vídeo usando pydub (caminho absoluto para evitar erro)
audio = AudioSegment.from_file(r"C:\Users\LuisaHamon\challenge-artificial-intelligence\resources\Dica do professor.mp4", format="mp4")
audio.export(r"C:\Users\LuisaHamon\challenge-artificial-intelligence\resources\dica.wav", format="wav")

wf = wave.open(r'C:\Users\LuisaHamon\challenge-artificial-intelligence\resources\dica.wav', "rb")
model = Model(r"C:\Users\LuisaHamon\Downloads\vosk-model-small-pt-0.3\vosk-model-small-pt-0.3")
rec = KaldiRecognizer(model, wf.getframerate())
transcricao = ""
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())
        transcricao += res.get('text', '') + ' '
wf.close()

# Conecta ao banco de dados principal
conn = sqlite3.connect('index.db')
c = conn.cursor()
# Cria a tabela se não existir, com restrição de unicidade para evitar duplicidade
c.execute('CREATE TABLE IF NOT EXISTS videos (id INTEGER PRIMARY KEY, titulo TEXT UNIQUE, transcricao TEXT)')
# Insere apenas se não existir vídeo com o mesmo título
c.execute('INSERT OR IGNORE INTO videos (titulo, transcricao) VALUES (?, ?)', ('Dica do professor', transcricao))
conn.commit()
conn.close()
