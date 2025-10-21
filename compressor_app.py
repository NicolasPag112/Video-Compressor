import customtkinter as ctk
from CompressorClass import CompressorApp


# Define a aparência padrão (pode ser "dark", "light")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    app = CompressorApp()
    app.mainloop()