from openwakeword.model import Model
import sounddevice as sd
import numpy as np

class WakeWordListener:
    def __init__(self, model_path: str = "models/wakewords/astra.onnx"):
        print("[WakeWord] Cargando modelo de openWakeWord...")
        self.model = Model(wakeword_models=[model_path])
        self.sample_rate = 16000
        self.chunk_size = 1280

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(f"[Aviso Audio] {status}")

        audio_data = np.frombuffer(indata, dtype=np.int16)
        self.model.predict(audio_data)

        for model_name in self.model.models:
            score = self.model.prediction_buffer[model_name][-1]
            if score > 0.3:
                print(f"\n[WAKE WORD DETECTADA!] Modelo: {model_name} (Confianza: {score:.2f})")

    def listen(self):
        print("[WakeWord] Escuchando ... llama a Astra o presiona Ctrl+C para salir.")

        with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype="int16",
                            blocksize=self.chunk_size, callback=self._audio_callback):
            try:
                while True:
                    sd.sleep(100)
            except KeyboardInterrupt:
                print("\n[WakeWord] Deteniendo escucha...")


if __name__ == "__main__":
    WakeWordListener().listen()