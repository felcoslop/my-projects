# my-projects

Coletânea de **scripts utilitários em Python** para tarefas do dia a dia: remoção de fundo de imagens, transcrição de áudio e download/conversão de vídeos do YouTube. Cada script é independente.

## Scripts

### 🖼️ `remove_bg.py` — Remoção de fundo em lote

Remove o fundo de todas as imagens de uma pasta usando **rembg**, salvando o resultado em PNG com transparência.

- Entrada: pasta `images/`
- Saída: pasta `removed_bg_images/`
- Formatos aceitos: `.png`, `.jpg`, `.jpeg`, `.webp`

```bash
pip install rembg pillow
python remove_bg.py
```

### 🎙️ `transcript_mp3.py` — Transcrição de áudio (MP3 → texto)

Converte um MP3 para WAV, divide em segmentos de 60s e transcreve usando o **Google Speech Recognition** (`speech_recognition`). O resultado é salvo em `transcription.txt`.

```bash
pip install SpeechRecognition pydub
# requer ffmpeg instalado
python transcript_mp3.py
```

> Ajuste o caminho do MP3 e o idioma (`language="en-US"`) dentro do script.

### ▶️ `ytb_v1de0_downloader_and_converter.py` — Downloader do YouTube

Baixa vídeos do YouTube (melhor qualidade em MP4) ou extrai só o áudio em **MP3 (192 kbps)**, via **yt-dlp**. Interface interativa no terminal: pede o link, o caminho de destino e o formato.

```bash
pip install yt-dlp
# requer ffmpeg instalado
python ytb_v1de0_downloader_and_converter.py
```

## Requisitos gerais

- Python 3.9+
- **ffmpeg** instalado no sistema (necessário para os scripts de áudio/vídeo)
- As dependências variam por script (veja acima).
