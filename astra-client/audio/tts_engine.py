import subprocess
import tempfile
import os
import sounddevice as sd
import soundfile as sf

def speak(text: str, model_path: str = "models/piper/es_AR-daniela-high.onnx"):
    """
    Sintetiza texto a voz usando Piper y lo reproduce por los altavoces.
    """
    if not text.strip():
        return

    print(f"[TTS] Sintetizando voz: '{text}'")
    
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_wav.close()

    try:
        result = subprocess.run(
            [
                "piper",
                "--model", str(model_path),
                "--length-scale", "1.2",
                "--output_file", str(temp_wav.name),
            ],
            input=text + "\n",
            text=True,
            capture_output=True,
        )
        
        if result.returncode != 0:
            print(f"[Error TTS] Fallo al generar la voz: {result.stderr}")
            return

        data, fs = sf.read(temp_wav.name)
        sd.play(data, fs)
        sd.wait()

    except Exception as e:
        print(f"[Error TTS] Excepción al reproducir audio: {e}")
    
    finally:
        if os.path.exists(temp_wav.name):
            os.unlink(temp_wav.name)