import tkinter as tk
from tkinter import messagebox, scrolledtext
import datetime
import random
import re

# ==================== CONFIGURAÇÕES DE TEMA ====================
TEMA_CLARO = {
    "bg": "#FFFFFF",
    "fg": "#000000",
    "button_bg": "#E5E5E5",
    "button_fg": "#000000",
    "button_hover": "#CCCCCC",
    "chat_bg": "#F5F5F5",
    "input_bg": "#FFFFFF",
    "user_bg": "#DCEAFE",
    "user_fg": "#003366",
    "bot_bg": "#F0F0F0",
    "bot_fg": "#000000"
}

TEMA_ESCURO = {
    "bg": "#1E1E1E",
    "fg": "#FFFFFF",
    "button_bg": "#2E2E2E",
    "button_fg": "#FFFFFF",
    "button_hover": "#444444",
    "chat_bg": "#2A2A2A",
    "input_bg": "#1E1E1E",
    "user_bg": "#003366",
    "user_fg": "#FFFFFF",
    "bot_bg": "#444444",
    "bot_fg": "#FFFFFF"
}

# Usuários permitidos
USUARIOS = {
    "admin": "admin123",
    "usuario": "senha123"
}

# Conhecimento básico do bot
CONHECIMENTO_TI = {
    "redes": {
        "perguntas": ["rede", "roteador", "ip", "dns", "gateway"],
        "resposta": "🌐 **Redes de Computadores**\n\nIP identifica um dispositivo. DNS traduz nomes para IPs. Gateway é o caminho para outras redes."
    },
    "python": {
        "perguntas": ["python", "lista", "dicionário", "função"],
        "resposta": "🐍 **Python** é uma linguagem simples e poderosa. Exemplo:\n```python\ndef somar(a, b):\n    return a + b\n```"
    },
    "oop": {
        "perguntas": ["poo", "oop", "classe", "objeto", "herança", "encapsulamento"],
        "resposta": "🏗️ **POO** organiza código usando classes e objetos.\nClasse = modelo, Objeto = instância."
    }
}

# ==================== CLASSE PRINCIPAL ====================
class ChatbotApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ChatBot IA - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.usuario_logado = None
        self.tema_atual = TEMA_CLARO
        self.modo_escuro = False

        self.criar_tela_login()

    def criar_tela_login(self):
        login_frame = tk.Frame(self.root, bg="#000000")
        login_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(login_frame, text="⚫ BLACKAI - TI", font=("Arial", 24, "bold"), bg="#000000", fg="white").pack(pady=30)

        campos_frame = tk.Frame(login_frame, bg="#000000")
        campos_frame.pack(pady=20)

        tk.Label(campos_frame, text="Usuário:", font=("Arial", 10), bg="#000000", fg="white").grid(row=0, column=0, sticky="w")
        self.entry_usuario = tk.Entry(campos_frame, width=25)
        self.entry_usuario.grid(row=0, column=1, pady=5)

        tk.Label(campos_frame, text="Senha:", font=("Arial", 10), bg="#000000", fg="white").grid(row=1, column=0, sticky="w")
        self.entry_senha = tk.Entry(campos_frame, width=25, show="●")
        self.entry_senha.grid(row=1, column=1, pady=5)
        self.entry_senha.bind("<Return>", lambda e: self.fazer_login())

        tk.Button(login_frame, text="Entrar", width=20, command=self.fazer_login).pack(pady=20)

        tk.Label(login_frame, text="💡 admin/admin123", font=("Arial", 8), bg="#000000", fg="white").pack()

    def fazer_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get()

        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            self.usuario_logado = usuario
            self.abrir_chat()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
            self.entry_senha.delete(0, tk.END)

    def abrir_chat(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(f"BLACKAI TI - {self.usuario_logado}")
        self.root.geometry("900x650")
        self.root.resizable(True, True)

        self.criar_interface_chat()
        self.aplicar_tema()

        self.adicionar_mensagem("bot", f"👋 Olá, {self.usuario_logado}! Como posso ajudar na TI hoje?")

    def criar_interface_chat(self):
        header_frame = tk.Frame(self.root)
        header_frame.pack(fill=tk.X)

        tk.Label(header_frame, text="⚫ BLACKAI - ASSISTENTE DE TI", font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=20)

        self.btn_tema = tk.Button(header_frame, text="🌙 Modo Escuro", command=self.alternar_tema)
        self.btn_tema.pack(side=tk.RIGHT)

        chat_frame = tk.Frame(self.root)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, pady=10)

        self.entry_mensagem = tk.Text(input_frame, height=3)
        self.entry_mensagem.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.entry_mensagem.bind("<Return>", self.enviar_mensagem_enter)

        tk.Button(input_frame, text="📤 Enviar", command=self.enviar_mensagem).pack(side=tk.RIGHT, padx=10)

    def enviar_mensagem_enter(self, event):
        if not event.state & 1:
            self.enviar_mensagem()
            return "break"

    def enviar_mensagem(self):
        mensagem = self.entry_mensagem.get("1.0", tk.END).strip()
        if not mensagem:
            return

        self.adicionar_mensagem("usuario", mensagem)
        self.entry_mensagem.delete("1.0", tk.END)
        self.root.after(500, lambda: self.gerar_resposta(mensagem))

    def adicionar_mensagem(self, remetente, texto):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n[{remetente.upper()}] {datetime.datetime.now().strftime('%H:%M')}\n{texto}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def detectar_topico_ti(self, mensagem):
        mensagem_lower = mensagem.lower()
        for topico, dados in CONHECIMENTO_TI.items():
            if any(p in mensagem_lower for p in dados["perguntas"]):
                return dados["resposta"]
        return None

    def gerar_resposta(self, mensagem):
        resposta = self.detectar_topico_ti(mensagem)
        if not resposta:
            resposta = "🤖 Não tenho certeza sobre isso, mas posso ajudar se detalhar melhor!"
        self.adicionar_mensagem("bot", resposta)

    def alternar_tema(self):
        self.modo_escuro = not self.modo_escuro
        self.tema_atual = TEMA_ESCURO if self.modo_escuro else TEMA_CLARO
        self.aplicar_tema()
        self.btn_tema.config(text="☀️ Modo Claro" if self.modo_escuro else "🌙 Modo Escuro")

    def aplicar_tema(self):
        tema = self.tema_atual
        self.root.config(bg=tema["bg"])
        self.chat_display.config(bg=tema["chat_bg"], fg=tema["fg"])
        self.entry_mensagem.config(bg=tema["input_bg"], fg=tema["fg"])

    def executar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ChatbotApp()
    app.executar()
