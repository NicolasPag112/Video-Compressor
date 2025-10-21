# CompressorClass.py
import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
import ffmpeg
import threading
import os
import datetime
import random


class CompressorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Dicionário de Traduções ---
        self.setup_translations()
        
        # --- Variável de Estado de Linguagem ---
        self.current_lang = ctk.StringVar(value="en") # 'en' como padrão

        # --- Configurações da Janela ---
        # Aumentei a altura para caber o seletor de linguagem
        self.geometry("500x650") 
        self.grid_columnconfigure(0, weight=1)

        self.video_path = None
        self.output_folder_path = None
        self.save_path = None 

        # --- Mapa de Resolução (sem tradução, são valores técnicos) ---
        self.resolution_map = {
            0: {"label": "480p", "height": 480},
            1: {"label": "720p", "height": 720},
            2: {"label": "1080p", "height": 1080}
        }
        
        # --- Variáveis de Estado da UI ---
        self.compression_mode = ctk.StringVar(value="CRF") 

        # --- Lógica de Inicialização ---
        self.set_default_output_folder() 
        self.create_widgets()
        self.set_video_selected_state(False) 
        self.update_ui_text() # Aplica o texto inicial

    def setup_translations(self):
        """Define todos os textos da UI em ambos os idiomas."""
        self.translations = {
            "en": {
                "title": "Video Compressor",
                "select_video_btn": "Select Video",
                "no_video_selected": "No video selected",
                "select_video_title": "Select a video file",
                "video_files": "Video Files",
                "all_files": "All Files",
                "output_folder_btn": "Output Folder",
                "select_folder_title": "Select the folder to save videos",
                "compression_method": "Compression Method:",
                "crf_radio": "CRF (Quality)",
                "bitrate_radio": "Bitrate (Size)",
                "res_radio": "Resolution (Dimensions)",
                "level_label": "Level:",
                "crf_slider_label": "CRF: {val} (Lower = Better Quality)",
                "bitrate_slider_label": "Bitrate: {val} kbits/s",
                "res_slider_label": "Height: {label}",
                "compress_btn": "Compress Video",
                "invalid_folder_error": "Error: Invalid output folder.",
                "compressing_status": "Compressing... Please wait.",
                "success_message": "Saved as {file}",
                "ffmpeg_error": "Compression error. (Check console)",
                "generic_error": "Error: {err}"
            },
            "pt": {
                "title": "Compactador de Vídeo",
                "select_video_btn": "Selecionar Vídeo",
                "no_video_selected": "Nenhum vídeo selecionado",
                "select_video_title": "Selecione um arquivo de vídeo",
                "video_files": "Arquivos de Vídeo",
                "all_files": "Todos os Arquivos",
                "output_folder_btn": "Pasta de Saída",
                "select_folder_title": "Selecione a pasta para salvar os vídeos",
                "compression_method": "Método de Compressão:",
                "crf_radio": "CRF (Qualidade)",
                "bitrate_radio": "Bitrate (Tamanho)",
                "res_radio": "Resolução (Dimensões)",
                "level_label": "Nível:",
                "crf_slider_label": "CRF: {val} (Menor = Melhor Qualidade)",
                "bitrate_slider_label": "Bitrate: {val} kbits/s",
                "res_slider_label": "Altura: {label}",
                "compress_btn": "Compactar Vídeo",
                "invalid_folder_error": "Erro: Pasta de saída inválida.",
                "compressing_status": "Compactando... Por favor, aguarde.",
                "success_message": "Salvo como {file}",
                "ffmpeg_error": "Erro na compressão. (Ver console)",
                "generic_error": "Erro: {err}"
            }
        }

    def create_widgets(self):
        # Pega as traduções da linguagem padrão (será atualizado depois)
        t = self.translations[self.current_lang.get()]

        # --- 0. Seletor de Linguagem (NOVO) ---
        self.frame_lang = ctk.CTkFrame(self)
        self.frame_lang.grid(row=0, column=0, padx=15, pady=(15, 0), sticky="ew")
        self.frame_lang.grid_columnconfigure(0, weight=1)

        self.lang_selector = ctk.CTkSegmentedButton(
            self.frame_lang,
            values=["en", "pt"],
            variable=self.current_lang,
            command=self.switch_language # Chama a função de troca
        )
        self.lang_selector.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # --- 1. Seleção de Arquivo ---
        self.frame_file = ctk.CTkFrame(self)
        self.frame_file.grid(row=1, column=0, padx=15, pady=15, sticky="ew") # row=1
        self.frame_file.grid_columnconfigure(1, weight=1)

        self.btn_select = ctk.CTkButton(self.frame_file, text=t['select_video_btn'], command=self.select_video)
        self.btn_select.grid(row=0, column=0, padx=10, pady=10)

        self.lbl_file = ctk.CTkLabel(self.frame_file, text=t['no_video_selected'], text_color="gray", anchor="w")
        self.lbl_file.grid(row=0, column=1, padx=10, sticky="ew")

        # --- 2. Seleção de Pasta de Saída ---
        self.frame_output = ctk.CTkFrame(self)
        self.frame_output.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="ew") # row=2
        self.frame_output.grid_columnconfigure(1, weight=1)

        self.btn_select_output = ctk.CTkButton(self.frame_output, text=t['output_folder_btn'], command=self.select_output_folder)
        self.btn_select_output.grid(row=0, column=0, padx=10, pady=10)

        self.lbl_output = ctk.CTkLabel(self.frame_output, text=self.output_folder_path, text_color="gray", anchor="w")
        self.lbl_output.grid(row=0, column=1, padx=10, sticky="ew")

        # --- 3. Opções de Compressão ---
        self.frame_options = ctk.CTkFrame(self)
        self.frame_options.grid(row=3, column=0, padx=15, pady=(0, 15), sticky="nsew") # row=3
        self.frame_options.grid_columnconfigure(1, weight=1)

        self.lbl_mode = ctk.CTkLabel(self.frame_options, text=t['compression_method'], font=ctk.CTkFont(weight="bold"))
        self.lbl_mode.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        self.radio_crf = ctk.CTkRadioButton(self.frame_options, text=t['crf_radio'], variable=self.compression_mode,
                                              value="CRF", command=self.update_slider_config)
        self.radio_crf.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        self.radio_bitrate = ctk.CTkRadioButton(self.frame_options, text=t['bitrate_radio'], variable=self.compression_mode,
                                                  value="Bitrate", command=self.update_slider_config)
        self.radio_bitrate.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        
        self.radio_res = ctk.CTkRadioButton(self.frame_options, text=t['res_radio'], variable=self.compression_mode,
                                              value="Resolução", command=self.update_slider_config)
        self.radio_res.grid(row=3, column=0, padx=20, pady=5, sticky="w")

        # --- 4. Slider de Nível ---
        self.lbl_level = ctk.CTkLabel(self.frame_options, text=t['level_label'], font=ctk.CTkFont(weight="bold"))
        self.lbl_level.grid(row=4, column=0, padx=10, pady=(15, 0), sticky="w")

        self.lbl_slider_value = ctk.CTkLabel(self.frame_options, text="", font=ctk.CTkFont(size=14)) # Texto definido por update_slider_label
        self.lbl_slider_value.grid(row=4, column=1, padx=10, pady=(15, 0), sticky="e")

        self.slider = ctk.CTkSlider(self.frame_options, from_=18, to=30, number_of_steps=12,
                                     command=self.update_slider_label)
        self.slider.set(23)
        self.slider.grid(row=5, column=0, columnspan=2, padx=10, pady=(5, 20), sticky="ew")

        # --- 5. Ação e Progresso ---
        self.btn_compress = ctk.CTkButton(self, text=t['compress_btn'], command=self.start_compression_thread, height=40)
        self.btn_compress.grid(row=4, column=0, padx=15, pady=10, sticky="ew") # row=4

        self.progress_bar = ctk.CTkProgressBar(self, mode="indeterminate")
        # (será mostrado/oculto na row=5)

        self.lbl_status = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12))
        self.lbl_status.grid(row=6, column=0, padx=15, pady=(5, 10), sticky="w") # row=6
    
    # --- Funções de Lógica da UI ---

    def switch_language(self, lang):
        """Chamado pelo seletor de linguagem para atualizar a UI."""
        self.update_ui_text()

    def update_ui_text(self):
        """Atualiza todo o texto visível da UI para a linguagem selecionada."""
        lang = self.current_lang.get()
        t = self.translations[lang]

        # Atualiza o título da janela
        self.title(t['title'])

        # Atualiza os botões
        self.btn_select.configure(text=t['select_video_btn'])
        self.btn_select_output.configure(text=t['output_folder_btn'])
        self.btn_compress.configure(text=t['compress_btn'])

        # Atualiza os labels estáticos
        self.lbl_mode.configure(text=t['compression_method'])
        self.lbl_level.configure(text=t['level_label'])

        # Atualiza os Radio Buttons
        self.radio_crf.configure(text=t['crf_radio'])
        self.radio_bitrate.configure(text=t['bitrate_radio'])
        self.radio_res.configure(text=t['res_radio'])
        
        # Atualiza os labels dinâmicos (com base no estado)
        if not self.video_path:
            self.lbl_file.configure(text=t['no_video_selected'])
        
        # Atualiza o texto do slider
        self.update_slider_label(self.slider.get())
        
        # (O lbl_output não precisa, pois mostra um caminho de pasta)
        # (O lbl_status é atualizado por outras funções)

    def set_default_output_folder(self):
        """Encontra a pasta 'Vídeos' do usuário e a define como padrão."""
        try:
            home = Path.home()
            videos_dir_pt = home / "Vídeos" # Português
            videos_dir_en = home / "Videos" # Inglês
            
            if videos_dir_pt.is_dir():
                self.output_folder_path = str(videos_dir_pt)
            elif videos_dir_en.is_dir():
                self.output_folder_path = str(videos_dir_en)
            else:
                self.output_folder_path = str(home)
        except Exception as e:
            print(f"Erro ao encontrar pasta de vídeos: {e}")
            self.output_folder_path = os.getcwd() 

    def set_video_selected_state(self, is_selected):
        state = "normal" if is_selected else "disabled"
        self.radio_crf.configure(state=state)
        self.radio_bitrate.configure(state=state)
        self.radio_res.configure(state=state)
        self.slider.configure(state=state)
        self.btn_compress.configure(state=state)

    def set_processing_state(self, is_processing):
        state = "disabled" if is_processing else "normal"
        
        self.btn_select.configure(state=state)
        self.btn_select_output.configure(state=state)
        self.lang_selector.configure(state=state) # Desabilita o seletor de idioma
        
        if not is_processing:
            self.set_video_selected_state(bool(self.video_path))
        else:
            self.set_video_selected_state(False)

    def select_video(self):
        """Abre a janela de diálogo (traduzida) para selecionar um vídeo."""
        t = self.translations[self.current_lang.get()]
        
        path = filedialog.askopenfilename(
            title=t['select_video_title'],
            filetypes=[
                (t['video_files'], "*.mp4 *.mkv *.mov *.avi"), 
                (t['all_files'], "*.*")
            ]
        )
        if path:
            self.video_path = path
            self.lbl_file.configure(text=os.path.basename(path), text_color="white")
            self.set_video_selected_state(True)
            self.update_slider_config()

    def select_output_folder(self):
        """Abre a janela de diálogo (traduzida) para selecionar uma pasta."""
        t = self.translations[self.current_lang.get()]
        
        path = filedialog.askdirectory(title=t['select_folder_title'])
        if path:
            self.output_folder_path = path
            self.lbl_output.configure(text=self.output_folder_path, text_color="white")

    def update_slider_config(self):
        """Atualiza a faixa do slider e chama o update do label."""
        mode = self.compression_mode.get()
        
        if mode == "CRF":
            self.slider.configure(from_=18, to=30, number_of_steps=12)
            self.slider.set(23)
        elif mode == "Bitrate":
            self.slider.configure(from_=500, to=5000, number_of_steps=45)
            self.slider.set(1500)
        elif mode == "Resolução":
            self.slider.configure(from_=0, to=2, number_of_steps=2)
            self.slider.set(1)
            
        self.update_slider_label(self.slider.get())

    def update_slider_label(self, value):
        """Atualiza o texto do slider (traduzido)."""
        t = self.translations[self.current_lang.get()]
        mode = self.compression_mode.get()
        val_int = int(value)
        
        label_text = ""
        if mode == "CRF":
            label_text = t['crf_slider_label'].format(val=val_int)
        elif mode == "Bitrate":
            label_text = t['bitrate_slider_label'].format(val=val_int)
        elif mode == "Resolução":
            label_key = self.resolution_map[val_int]['label']
            label_text = t['res_slider_label'].format(label=label_key)
            
        self.lbl_slider_value.configure(text=label_text)

    # --- Funções de Compressão (Threading) ---

    def start_compression_thread(self):
        """Inicia a compressão (com mensagens traduzidas)."""
        t = self.translations[self.current_lang.get()]
        
        if not self.video_path:
            return

        # 1. Gerar nome de arquivo
        base_name_full = os.path.basename(self.video_path)
        original_name, _ = os.path.splitext(base_name_full)
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        unique_code = f"{random.randint(100000, 999999)}"
        file_name = f"{original_name}_{timestamp}_{unique_code}.mp4"

        # 2. Verificar pasta
        if not self.output_folder_path or not os.path.isdir(self.output_folder_path):
            self.lbl_status.configure(text=t['invalid_folder_error'], text_color="red")
            return

        self.save_path = os.path.join(self.output_folder_path, file_name)

        # 3. Desabilitar UI e mostrar progresso
        self.set_processing_state(True) 
        self.lbl_status.configure(text=t['compressing_status'], text_color="white")
        self.progress_bar.grid(row=5, column=0, padx=15, pady=10, sticky="ew") # row=5
        self.progress_bar.start()

        # 4. Iniciar thread
        compress_thread = threading.Thread(target=self.run_compression)
        compress_thread.daemon = True
        compress_thread.start()

    def run_compression(self):
        """Executa o comando FFmpeg. (NÃO CHAME DIRETAMENTE DA UI)"""
        mode = self.compression_mode.get()
        slider_value = int(self.slider.get())
        
        try:
            in_file = ffmpeg.input(self.video_path)
            in_audio = in_file.audio
            in_video = in_file.video

            output_params = {"c:a": "copy", "preset": "fast"}

            if mode == "CRF":
                output_params["crf"] = slider_value
            elif mode == "Bitrate":
                output_params["b:v"] = f"{slider_value}k"
            elif mode == "Resolução":
                height = self.resolution_map[slider_value]["height"]
                in_video = in_video.filter('scale', -2, height)

            out = ffmpeg.output(in_video, in_audio, self.save_path, **output_params)
            ffmpeg.run(out, overwrite_output=True)
            
            final_file_name = os.path.basename(self.save_path) 
            
            # Sucesso: Passa a chave 'success' e o nome do arquivo
            self.after(0, self.on_compression_finished, 'success', 'green', final_file_name)

        except ffmpeg.Error as e:
            error_message = e.stderr.decode()
            print("Erro no FFmpeg:", error_message)
            # Erro FFmpeg: Passa a chave 'ffmpeg_error'
            self.after(0, self.on_compression_finished, 'ffmpeg_error', 'red')
        except Exception as e:
             print("Erro inesperado:", str(e))
             # Erro Genérico: Passa a chave 'generic_error' e a mensagem
             self.after(0, self.on_compression_finished, 'generic_error', 'red', str(e))


    def on_compression_finished(self, message_key, color, data=None):
        """Chamado quando a compressão termina (traduz a mensagem final)."""
        self.progress_bar.stop()
        self.progress_bar.grid_forget()
        
        t = self.translations[self.current_lang.get()]
        message = ""

        # Monta a mensagem final traduzida
        if message_key == 'success':
            message = t['success_message'].format(file=data)
        elif message_key == 'ffmpeg_error':
            message = t['ffmpeg_error']
        elif message_key == 'generic_error':
            message = t['generic_error'].format(err=data)
        
        self.lbl_status.configure(text=message, text_color=color)
        
        # Destrava a UI
        self.set_processing_state(False)