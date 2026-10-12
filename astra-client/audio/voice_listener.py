import queue
import sys
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

class VoiceListener:
    def __init__(self, model_path: str = "models/vosk/vosk-model-es-0.42"):
        print(f"[Audio] Cargando modelo de Vosk desde '{model_path}'...")
        if not Model:
            raise ImportError("La librería vosk no está instalada.")
        
        self.model = Model(model_path)
        self.samplerate = 16000  # Frecuencia estándar para Vosk
        self.q = queue.Queue()

    def _callback(self, indata, frames, time, status):
        """Cola para recibir los bloques de audio del micrófono."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def listen_once(self) -> str:
        """Escucha el micrófono hasta capturar una frase completa y la devuelve transcrita. """
        print("\n[Escuchando...] (Habla ahora)")
        
        # Abrir microfono
        with sd.RawInputStream(samplerate=self.samplerate, blocksize=8000, dtype='int16',
                               channels=1, callback=self._callback):
            
            rec = KaldiRecognizer(self.model, self.samplerate)
            
            while True:
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "").strip()
                    if text:
                        print(f"[Voz Reconocida] > {text}")
                        return text
