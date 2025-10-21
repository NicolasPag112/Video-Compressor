# run.py
import os
import sys
import subprocess

VENV_DIR = "venv"

def get_venv_python():
    """Retorna o caminho para o executável Python dentro da venv, baseado no SO."""
    if sys.platform == "win32":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    else: # macOS / Linux
        return os.path.join(VENV_DIR, "bin", "python")

def create_venv(venv_python_path):
    """Cria o ambiente virtual."""
    print(f"Criando ambiente virtual em '{VENV_DIR}'...")
    # Usa o executável Python atual (que está rodando este script) para criar a venv
    try:
        subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)
        print("Ambiente virtual criado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"ERRO: Falha ao criar ambiente virtual. {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("ERRO: Python não encontrado. Verifique sua instalação.")
        sys.exit(1)

def install_dependencies(venv_python):
    """Instala as dependências usando o pip da venv a partir do requirements.txt."""
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"ERRO: Arquivo '{requirements_file}' não encontrado.")
        print("Certifique-se de que o arquivo com as dependências está na mesma pasta do run.py.")
        sys.exit(1)
        
    print(f"Instalando/verificando dependências a partir de '{requirements_file}'...")
    try:
        subprocess.run(
            [venv_python, "-m", "pip", "install", "-r", requirements_file],
            check=True,
            capture_output=True, # Suprime a saída longa do pip
            text=True
        )
        print("Dependências instaladas com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"ERRO: Falha ao instalar dependências.")
        print(e.stderr)
        sys.exit(1)

def launch_app(venv_python):
    """Inicia a aplicação principal."""
    print("Iniciando o Compressor de Vídeo...")
    try:
        # Executa o compressor_app.py usando o Python da venv
        subprocess.run([venv_python, "compressor_app.py"])
    except Exception as e:
        print(f"ERRO: Falha ao iniciar a aplicação. {e}")
        sys.exit(1)

def main():
    # 1. Define o caminho do executável da venv
    venv_python = get_venv_python()

    # 2. Verifica se a venv existe
    if not os.path.exists(venv_python):
        create_venv(venv_python)
    
    # 3. Instala/verifica as dependências
    # (O pip é inteligente, ele só baixa se for necessário)
    install_dependencies(venv_python)

    # 4. Inicia a aplicação
    launch_app(venv_python)

if __name__ == "__main__":
    main()