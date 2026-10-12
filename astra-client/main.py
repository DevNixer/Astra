import sys
from audio.tts_engine import speak

def print_banner():
    print("=" * 50)
    print("                    ASTRA - CLIENT                   ")
    print("=" * 50)
    print("Escribe texto o usa comandos:")
    print("  /exit           - Sale de la aplicación.")
    print("  /speak <texto>  - Hace que Astra hable el texto indicado.")
    print("  /help           - Muestra esta ayuda.")
    print("=" * 50)

def main():
    print_banner()

    while True:
        try:
            user_input = input("\n[Tú] > ").strip()
            
            if not user_input:
                continue
            
            # Gestionar comandos 
            if user_input.startswith("/"):
                parts = user_input.split(" ", 1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if command == "/exit":
                    print("\n[Astra] Apagando sistema. ¡Hasta pronto!")
                    sys.exit(0)
                    
                elif command == "/help":
                    print_banner()
                    continue
                    
                elif command == "/speak":
                    if not args:
                        print("[Sistema] Error: Debes escribir texto después de /speak.")
                        continue
                    speak(args)
                    continue
                
                else:
                    print(f"[Sistema] Comando desconocido '{command}'. Escribe /help para ver los ayudas.")
                    continue
            
            # Procesamiento de mensajes normales
            response = f"He recibido el texto: '{user_input}'."
            print(f"[Astra] > {response}")
            
        except KeyboardInterrupt:
            print("\n\n[Astra] Sesión interrumpida. Saliendo...")
            break

if __name__ == "__main__":
    main()