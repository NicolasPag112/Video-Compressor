# Video Compressor GUI

A simple and modern desktop app for compressing videos using FFmpeg, built with Python and CustomTkinter.

This application provides a user-friendly graphical interface (GUI) to compress video files. It leverages the power of FFmpeg to offer multiple compression methods (CRF, Bitrate, Resolution) and runs the compression in a separate thread to prevent the UI from freezing.

The app features an automatic setup script, internationalization (English and Portuguese), and smart file/folder handling.

## Features

  * **Modern UI:** Clean, dark-mode interface built with CustomTkinter.
  * **Multi-language Support:** Toggle between English and Portuguese with instant UI updates.
  * **Three Compression Modes:**
      * **CRF (Quality):** Adjust the Constant Rate Factor for quality-based compression.
      * **Bitrate (Size):** Set a specific video bitrate to control file size.
      * **Resolution (Dimensions):** Resize the video to 480p, 720p, or 1080p.
  * **Asynchronous Processing:** Compression runs in a separate thread, so the UI never freezes or lags.
  * **Smart File Handling:**
      * Automatically detects the system's 'Videos' folder as the default output.
      * Generates unique, timestamped filenames (e.g., `my_video_20251021_123456.mp4`) to prevent overwriting files.
  * **Automatic Setup:** A `run.py` script handles virtual environment creation and dependency installation automatically.

## Prerequisites

Before you begin, you must have the following installed on your system:

1.  **Python 3.7+**
2.  **FFmpeg:** This is essential. The app is a graphical front-end for FFmpeg and **will not work** without it.
      * **Windows:** The easiest way is using a package manager like [Chocolatey](https://chocolatey.org/):
        ```bash
        choco install ffmpeg
        ```
      * **macOS:** Use [Homebrew](https://brew.sh/):
        ```bash
        brew install ffmpeg
        ```
      * **Linux (Ubuntu/Debian):**
        ```bash
        sudo apt update
        sudo apt install ffmpeg
        ```

## Installation & Usage

This project includes an automatic setup script (`run.py`) that handles the creation of a virtual environment and the installation of dependencies.

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/NicolasPag112/Video-Compressor.git
    cd Video-Compressor
    ```

2.  **Run the application:**

    ```bash
    python run.py
    ```

The first time you run this command, it will automatically:

  * Create a virtual environment in a folder named `venv`.
  * Install all required libraries from `requirements.txt`.
  * Launch the application.

Every subsequent time you run `python run.py`, it will simply detect the existing environment and launch the application immediately.

## Technology Stack

  * **Python:** The core programming language.
  * **CustomTkinter:** For the modern GUI components.
  * **ffmpeg-python:** A Python wrapper for the FFmpeg command-line tool.

-----


-----

# Compressor de Vídeo (GUI)

Um aplicativo de desktop simples e moderno para comprimir vídeos usando FFmpeg, construído com Python e CustomTkinter.

Esta aplicação fornece uma interface gráfica (GUI) amigável para comprimir arquivos de vídeo. Ela utiliza o poder do FFmpeg para oferecer múltiplos métodos de compressão (CRF, Bitrate, Resolução) e executa a compressão em uma thread separada para evitar que a UI congele.

O aplicativo conta com um script de instalação automática, internacionalização (Inglês e Português) e gerenciamento inteligente de arquivos e pastas.

## Recursos

  * **UI Moderna:** Interface limpa e com dark-mode, construída com CustomTkinter.
  * **Suporte a Múltiplos Idiomas:** Alterne entre Inglês e Português com atualização instantânea da UI.
  * **Três Modos de Compressão:**
      * **CRF (Qualidade):** Ajuste o Fator de Taxa Constante (CRF) para compressão baseada em qualidade.
      * **Bitrate (Tamanho):** Defina uma taxa de bits (bitrate) específica para controlar o tamanho do arquivo.
      * **Resolução (Dimensões):** Redimensione o vídeo para 480p, 720p ou 1080p.
  * **Processamento Assíncrono:** A compressão roda em uma thread separada, para que a UI nunca congele ou trave.
  * **Gerenciamento Inteligente de Arquivos:**
      * Detecta automaticamente a pasta 'Vídeos' do sistema como saída padrão.
      * Gera nomes de arquivo únicos com data e hora (ex: `meu_video_20251021_123456.mp4`) para evitar sobreescrever arquivos.
  * **Instalação Automática:** Um script `run.py` cuida da criação do ambiente virtual e da instalação de dependências automaticamente.

## Pré-requisitos

Antes de começar, você deve ter o seguinte instalado em seu sistema:

1.  **Python 3.7+**
2.  **FFmpeg:** Essencial. O aplicativo é uma interface gráfica para o FFmpeg e **não funcionará** sem ele.
      * **Windows:** A forma mais fácil é usar um gerenciador de pacotes como [Chocolatey](https://chocolatey.org/):
        ```bash
        choco install ffmpeg
        ```
      * **macOS:** Use [Homebrew](https://brew.sh/):
        ```bash
        brew install ffmpeg
        ```
      * **Linux (Ubuntu/Debian):**
        ```bash
        sudo apt update
        sudo apt install ffmpeg
        ```

## Instalação e Uso

Este projeto inclui um script de configuração automática (`run.py`) que cuida da criação do ambiente virtual e da instalação das dependências.

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/NicolasPag112/Video-Compressor.git
    cd Video-Compressor
    ```

2.  **Execute a aplicação:**

    ```bash
    python run.py
    ```

Na primeira vez que você executar este comando, ele irá automaticamente:

  * Criar um ambiente virtual em uma pasta chamada `venv`.
  * Instalar todas as bibliotecas necessárias a partir do `requirements.txt`.
  * Iniciar a aplicação.

Em todas as execuções seguintes, o `python run.py` irá detectar o ambiente existente e iniciar a aplicação imediatamente.

## Tecnologias Utilizadas

  * **Python:** Linguagem de programação principal.
  * **CustomTkinter:** Para os componentes gráficos modernos da GUI.
  * **ffmpeg-python:** Um wrapper Python para a ferramenta de linha de comando FFmpeg.