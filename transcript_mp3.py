import speech_recognition as sr
import os
from pydub import AudioSegment
import math

def convert_mp3_to_wav(mp3_path, output_dir=None):
    """
    Converte MP3 para WAV, já que speech_recognition trabalha melhor com WAV
    """
    # Carrega o arquivo MP3
    audio = AudioSegment.from_mp3(mp3_path)
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.basename(mp3_path).replace('.mp3', '.wav')
        wav_path = os.path.join(output_dir, filename)
    else:
        wav_path = mp3_path.replace('.mp3', '.wav')
    
    audio.export(wav_path, format="wav")
    return wav_path

def split_audio(wav_path, segment_length_ms=60000):
    """
    Divide o áudio em segmentos menores (padrão: 60 segundos)
    """
    audio = AudioSegment.from_wav(wav_path)
    duration_ms = len(audio)
    
    # Calcula quantos segmentos serão criados
    num_segments = math.ceil(duration_ms / segment_length_ms)
    segments = []
    
    for i in range(num_segments):
        start = i * segment_length_ms
        end = min((i + 1) * segment_length_ms, duration_ms)
        segment = audio[start:end]
        segment_path = f"temp_segment_{i}.wav"
        segment.export(segment_path, format="wav")
        segments.append(segment_path)
    
    return segments

def transcribe_audio(mp3_path):
    """
    Função principal que transcreve o áudio MP3
    """
    try:
        # Inicializa o reconhecedor
        recognizer = sr.Recognizer()
        
        # Converte MP3 para WAV
        print("Convertendo MP3 para WAV...")
        wav_path = convert_mp3_to_wav(mp3_path, output_dir="temp_wav")
        
        # Divide o áudio em segmentos
        print("Dividindo áudio em segmentos...")
        segments = split_audio(wav_path)
        
        full_transcription = ""
        
        # Processa cada segmento
        for i, segment_path in enumerate(segments):
            print(f"Transcrevendo segmento {i + 1} de {len(segments)}...")
            
            with sr.AudioFile(segment_path) as source:
                # Ajusta para ruído ambiente
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.record(source)
                
                try:
                    # Tenta transcrever usando Google Speech Recognition
                    text = recognizer.recognize_google(audio, language="en-US")
                    full_transcription += text + " "
                except sr.UnknownValueError:
                    print(f"Segmento {i + 1}: Não foi possível entender o áudio")
                except sr.RequestError as e:
                    print(f"Segmento {i + 1}: Erro na requisição; {e}")
            
            # Remove o arquivo de segmento temporário
            os.remove(segment_path)
        
        # Remove o arquivo WAV temporário
        os.remove(wav_path)
        
        return full_transcription.strip()
    
    except Exception as e:
        return f"Ocorreu um erro: {str(e)}"

def main():
    # Caminho do arquivo MP3 (substitua pelo seu caminho)
    mp3_file = '/home/felipe/flink_playground/.mp3_source/audio_to_convert.mp3'
    
    if not os.path.exists(mp3_file):
        print("Arquivo MP3 não encontrado!")
        return
    
    print("Iniciando transcrição...")
    transcription = transcribe_audio(mp3_file)
    
    # Salva a transcrição em um arquivo de texto
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(transcription)
    
    print("\nTranscrição concluída! Resultado:")
    print(transcription)
    print("A transcrição também foi salva em 'transcription.txt'")

if __name__ == "__main__":
    main()