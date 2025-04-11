import os
import sys
from pathlib import Path
import yt_dlp
from typing import Optional

def clear_terminal():
    """Limpa o terminal de forma compatível com diferentes sistemas operacionais."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_url() -> Optional[str]:
    """Solicita e valida um URL do YouTube."""
    url = input("Digite o link do YouTube (ou 'sair' para encerrar): ").strip()
    if url.lower() == 'sair':
        return None
    # Verifica se parece ser um URL válido
    if not url.startswith(('https://', 'http://')) or 'youtube.com' not in url:
        print("Erro: Insira um link válido do YouTube.")
        return get_valid_url()
    return url

def get_save_path() -> Path:
    """Solicita o caminho para salvar o arquivo e valida."""
    while True:
        save_path = input("Digite o caminho para salvar (ex: /home/usuario/downloads): ").strip()
        save_path = Path(save_path)
        try:
            # Verifica se o diretório existe ou pode ser criado
            save_path.mkdir(parents=True, exist_ok=True)
            return save_path
        except Exception as e:
            print(f"Erro: Caminho inválido ({e}). Tente novamente.")

def get_download_format() -> str:
    """Solicita o formato desejado (vídeo ou MP3)."""
    while True:
        choice = input("Deseja baixar como [1] Vídeo ou [2] MP3? ").strip()
        if choice in ['1', '2']:
            return 'video' if choice == '1' else 'mp3'
        print("Erro: Escolha 1 para Vídeo ou 2 para MP3.")

def download_youtube(url: str, save_path: Path, download_format: str) -> bool:
    """Faz o download do vídeo ou converte para MP3."""
    try:
        # Configurações base do yt-dlp
        ydl_opts = {
            'outtmpl': str(save_path / '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': False,
            'progress': True,
        }

        if download_format == 'video':
            # Configurações para baixar vídeo (melhor qualidade disponível)
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
            })
        else:
            # Configurações para baixar apenas áudio e converter para MP3
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Baixando: {url}")
            ydl.download([url])
            print("Download concluído com sucesso!")
            return True

    except yt_dlp.utils.DownloadError as e:
        print(f"Erro ao baixar: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False

def main():
    """Função principal que gerencia o loop de downloads."""
    clear_terminal()
    print("=== Downloader de YouTube ===")
    print("Digite 'sair' a qualquer momento para encerrar.\n")

    while True:
        # Solicita URL
        url = get_valid_url()
        if url is None:
            print("Encerrando programa...")
            break

        # Solicita caminho para salvar
        save_path = get_save_path()

        # Solicita formato (vídeo ou MP3)
        download_format = get_download_format()

        # Faz o download
        success = download_youtube(url, save_path, download_format)

        if success:
            print(f"Arquivo salvo em: {save_path}")
        else:
            print("Falha no download. Verifique o link ou sua conexão.")

        # Pergunta se quer continuar
        continue_choice = input("\nDeseja baixar outro vídeo? [s/n]: ").strip().lower()
        if continue_choice != 's':
            print("Encerrando programa...")
            break

        clear_terminal()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")
        sys.exit(0)
