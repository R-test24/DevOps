import customtkinter as ctk
from tkinter import messagebox
import datetime
import mysql.connector
from mysql.connector import Error

# ─────────────────────────────────────────────
#  Conexão com banco
# ─────────────────────────────────────────────
def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost", user="root",
            password="root", database="gav_testepi"
        )
    except Error as e:
        messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao MySQL:\n{e}")
        return None

# ─────────────────────────────────────────────
#  Tema
# ─────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

AZUL     = "#2563EB"
AZUL_ESC = "#1D4ED8"
VERDE    = "#16A34A"
VERMELHO = "#DC2626"
LARANJA  = "#D97706"
BG       = "#0F172A"
CARD     = "#1E293B"
BORDA    = "#334155"
TEXTO    = "#F1F5F9"
SUBTEXTO = "#94A3B8"

# ─────────────────────────────────────────────
#  Helpers de UI
# ─────────────────────────────────────────────
def label(pai, texto, tamanho=13, cor=TEXTO, bold=False, anchor="w"):
    weight = "bold" if bold else "normal"
    return ctk.CTkLabel(pai, text=texto,
                        font=ctk.CTkFont(size=tamanho, weight=weight),
                        text_color=cor, anchor=anchor)

def entry(pai, placeholder="", width=280):
    return ctk.CTkEntry(pai, placeholder_text=placeholder, width=width,
                        fg_color=BG, border_color=BORDA, text_color=TEXTO,
                        placeholder_text_color=SUBTEXTO, corner_radius=8)

def btn(pai, texto, comando, cor=AZUL, hover=AZUL_ESC, width=140):
    return ctk.CTkButton(pai, text=texto, command=comando,
                         fg_color=cor, hover_color=hover,
                         corner_radius=8, width=width,
                         font=ctk.CTkFont(size=13, weight="bold"))

def combo(pai, valores, width=280):
    return ctk.CTkComboBox(pai, values=valores, width=width,
                           fg_color=BG, border_color=BORDA,
                           button_color=AZUL, button_hover_color=AZUL_ESC,
                           text_color=TEXTO, dropdown_fg_color=CARD,
                           corner_radius=8)

def separador(pai):
    ctk.CTkFrame(pai, height=1, fg_color=BORDA).pack(fill="x", padx=20, pady=8)

def form_campo(form, rotulo, widget):
    """Empacota label + widget num frame row dentro do form."""
    row = ctk.CTkFrame(form, fg_color="transparent")
    row.pack(fill="x", padx=24, pady=5)
    label(row, rotulo, 12, SUBTEXTO).pack(anchor="w")
    widget.pack(anchor="w", pady=(2, 0))

# ─────────────────────────────────────────────
#  Funções da Calculadora
# ─────────────────────────────────────────────
def arredondar_preco(valor: float) -> float:
    """Arredonda preço para o centavo .90 ou .00 mais próximo."""
    inteiro = int(valor)
    decimal = valor - inteiro
    if decimal <= 0.45:
        return inteiro + 0.00
    elif decimal <= 0.95:
        return inteiro + 0.90
    else:
        return inteiro + 1.00

# ─────────────────────────────────────────────
#  Janela principal
# ─────────────────────────────────────────────
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Estoque")
        self.geometry("1100x680")
        self.configure(fg_color=BG)
        self.resizable(True, True)
        self._build()

    def _build(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=CARD, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        label(self.sidebar, "📦  Estoque", 18, TEXTO, True).pack(pady=(30, 4), padx=20, anchor="w")
        label(self.sidebar, "Gestão de loja", 11, SUBTEXTO).pack(padx=20, anchor="w")
        ctk.CTkFrame(self.sidebar, height=1, fg_color=BORDA).pack(fill="x", padx=16, pady=18)

        # Botão Estoque (principal)
        self.btn_estoque = ctk.CTkButton(
            self.sidebar, text="📦  Estoque  ▼",
            command=lambda: self._toggle_submenu("estoque"),
            fg_color=AZUL, hover_color=AZUL_ESC,
            anchor="w", height=40, corner_radius=8,
            font=ctk.CTkFont(size=13), text_color=TEXTO
        )
        self.btn_estoque.pack(fill="x", padx=10, pady=2)

        # Frame para sub-itens do Estoque
        self.submenu_estoque = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        
        sub_itens_estoque = [
            ("🏠  Início", lambda: self._mostrar_sub_aba_estoque("inicio")),
            ("➕  Cadastrar", lambda: self._mostrar_sub_aba_estoque("cadastrar")),
            ("🔍  Consultar", lambda: self._mostrar_sub_aba_estoque("consultar")),
            ("✏️  Editar", lambda: self._mostrar_sub_aba_estoque("editar")),
            ("📈  Adicionar", lambda: self._mostrar_sub_aba_estoque("adicionar")),
            ("📉  Remover", lambda: self._mostrar_sub_aba_estoque("remover")),
        ]
        
        self.btn_sub_estoque = {}
        for texto, cmd in sub_itens_estoque:
            key = texto.split()[-1].lower() if texto.split()[-1].lower() != "início" else "inicio"
            btn = ctk.CTkButton(
                self.submenu_estoque, text="    " + texto,
                command=cmd,
                fg_color="transparent", hover_color=BORDA,
                anchor="w", height=32, corner_radius=4,
                font=ctk.CTkFont(size=11), text_color=SUBTEXTO
            )
            btn.pack(fill="x", padx=10, pady=1)
            self.btn_sub_estoque[key] = btn

        # Botão Fornecedores (principal)
        self.btn_fornecedores = ctk.CTkButton(
            self.sidebar, text="🏢  Fornecedores  ▶",
            command=lambda: self._toggle_submenu("fornecedores"),
            fg_color="transparent", hover_color=BORDA,
            anchor="w", height=40, corner_radius=8,
            font=ctk.CTkFont(size=13), text_color=SUBTEXTO
        )
        self.btn_fornecedores.pack(fill="x", padx=10, pady=2)

        # Frame para sub-itens dos Fornecedores
        self.submenu_fornecedores = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        
        sub_itens_fornecedores = [
            ("📋  Listar", lambda: self._mostrar_sub_aba_fornecedores("listar")),
            ("➕  Cadastrar", lambda: self._mostrar_sub_aba_fornecedores("cadastrar")),
            ("✏️  Editar", lambda: self._mostrar_sub_aba_fornecedores("editar")),
        ]
        
        self.btn_sub_fornecedores = {}
        for texto, cmd in sub_itens_fornecedores:
            key = texto.split()[-1].lower()
            btn = ctk.CTkButton(
                self.submenu_fornecedores, text="    " + texto,
                command=cmd,
                fg_color="transparent", hover_color=BORDA,
                anchor="w", height=32, corner_radius=4,
                font=ctk.CTkFont(size=11), text_color=SUBTEXTO
            )
            btn.pack(fill="x", padx=10, pady=1)
            self.btn_sub_fornecedores[key] = btn

        # Botão Precificação 
        self.btn_calculadora = ctk.CTkButton(
            self.sidebar, text="🧮  Precificação",
            command=lambda: self._mostrar_aba("Precificação"),
            fg_color="transparent", hover_color=BORDA,
            anchor="w", height=40, corner_radius=8,
            font=ctk.CTkFont(size=13), text_color=SUBTEXTO
        )
        self.btn_calculadora.pack(fill="x", padx=10, pady=(10,2))

        # Container principal
        self.container = ctk.CTkFrame(self, fg_color=BG)
        self.container.pack(side="left", fill="both", expand=True)

        # Frames das abas
        self.frame_estoque = ctk.CTkScrollableFrame(self.container, fg_color=BG, corner_radius=0)
        self.frame_fornecedores = ctk.CTkScrollableFrame(self.container, fg_color=BG, corner_radius=0)
        self.frame_calculadora = ctk.CTkScrollableFrame(self.container, fg_color=BG, corner_radius=0)

        # Conteúdo do Estoque
        self.content_estoque = ctk.CTkFrame(self.frame_estoque, fg_color="transparent")
        self.content_estoque.pack(fill="both", expand=True, padx=30, pady=10)

        # Conteúdo dos Fornecedores
        self.content_fornecedores = ctk.CTkFrame(self.frame_fornecedores, fg_color="transparent")
        self.content_fornecedores.pack(fill="both", expand=True, padx=30, pady=10)

        # Conteúdo da Calculadora
        self.content_calculadora = ctk.CTkFrame(self.frame_calculadora, fg_color="transparent")
        self.content_calculadora.pack(fill="both", expand=True, padx=30, pady=10)

        # Estado dos submenus
        self.submenu_aberto = "estoque"
        
        # Mostrar aba inicial
        self._mostrar_aba("estoque")
        self._mostrar_sub_aba_estoque("inicio")

    def _toggle_submenu(self, menu):
        """Alterna a exibição do submenu"""
        # Fecha o submenu da calculadora se estiver aberto
        self.btn_calculadora.configure(fg_color="transparent", text_color=SUBTEXTO)
        
        if menu == "estoque":
            if self.submenu_aberto == "estoque":
                self.submenu_estoque.pack_forget()
                self.btn_estoque.configure(text="📦  Estoque  ▶", fg_color="transparent", text_color=SUBTEXTO)
                self.submenu_aberto = None
            else:
                self.submenu_fornecedores.pack_forget()
                self.btn_fornecedores.configure(text="🏢  Fornecedores  ▶", fg_color="transparent", text_color=SUBTEXTO)
                
                self.submenu_estoque.pack(fill="x", pady=(5,10), after=self.btn_estoque)
                self.btn_estoque.configure(text="📦  Estoque  ▼", fg_color=AZUL, text_color=TEXTO)
                self.submenu_aberto = "estoque"
                self._mostrar_aba("estoque")
                
        elif menu == "fornecedores":
            if self.submenu_aberto == "fornecedores":
                self.submenu_fornecedores.pack_forget()
                self.btn_fornecedores.configure(text="🏢  Fornecedores  ▶", fg_color="transparent", text_color=SUBTEXTO)
                self.submenu_aberto = None
            else:
                self.submenu_estoque.pack_forget()
                self.btn_estoque.configure(text="📦  Estoque  ▶", fg_color="transparent", text_color=SUBTEXTO)
                
                self.submenu_fornecedores.pack(fill="x", pady=(5,10), after=self.btn_fornecedores)
                self.btn_fornecedores.configure(text="🏢  Fornecedores  ▼", fg_color=AZUL, text_color=TEXTO)
                self.submenu_aberto = "fornecedores"
                self._mostrar_aba("fornecedores")

    def _mostrar_aba(self, aba):
        """Mostra a aba selecionada"""
        self.frame_estoque.pack_forget()
        self.frame_fornecedores.pack_forget()
        self.frame_calculadora.pack_forget()
        
        # Fecha todos os submenus
        self.submenu_estoque.pack_forget()
        self.submenu_fornecedores.pack_forget()
        
        # Reseta todos os botões
        self.btn_estoque.configure(fg_color="transparent", text_color=SUBTEXTO, text="📦  Estoque  ▶")
        self.btn_fornecedores.configure(fg_color="transparent", text_color=SUBTEXTO, text="🏢  Fornecedores  ▶")
        self.btn_calculadora.configure(fg_color="transparent", text_color=SUBTEXTO)
        
        self.submenu_aberto = None
        
        if aba == "estoque":
            self.frame_estoque.pack(fill="both", expand=True)
            self.btn_estoque.configure(fg_color=AZUL, text_color=TEXTO, text="📦  Estoque  ▼")
            self.submenu_estoque.pack(fill="x", pady=(5,10), after=self.btn_estoque)
            self.submenu_aberto = "estoque"
        elif aba == "fornecedores":
            self.frame_fornecedores.pack(fill="both", expand=True)
            self.btn_fornecedores.configure(fg_color=AZUL, text_color=TEXTO, text="🏢  Fornecedores  ▼")
            self.submenu_fornecedores.pack(fill="x", pady=(5,10), after=self.btn_fornecedores)
            self.submenu_aberto = "fornecedores"
        elif aba == "Precificação":
            self.frame_calculadora.pack(fill="both", expand=True)
            self.btn_calculadora.configure(fg_color=AZUL, text_color=TEXTO)
            self._pg_calculadora(self.content_calculadora)

    # ═══════════════════════════════════════════
    #  ABA ESTOQUE
    # ═══════════════════════════════════════════

    def _mostrar_sub_aba_estoque(self, key):
        """Mostra a sub-aba selecionada no estoque"""
        for k, btn in self.btn_sub_estoque.items():
            btn.configure(fg_color=AZUL if k == key else "transparent",
                         text_color=TEXTO if k == key else SUBTEXTO)

        for w in self.content_estoque.winfo_children():
            w.destroy()

        f = self.content_estoque

        if key == "inicio":
            self._estoque_inicio(f)
        elif key == "cadastrar":
            self._pg_cadastrar_item(f)
        elif key == "consultar":
            self._pg_consultar_item(f)
        elif key == "editar":
            self._pg_editar_item(f)
        elif key == "adicionar":
            self._pg_movimentar_item(f, True)
        elif key == "remover":
            self._pg_movimentar_item(f, False)

    def _estoque_inicio(self, f):
        label(f, "Bem-vindo ao Módulo de Estoque", 22, TEXTO, True).pack(pady=(30,4), anchor="w")
        label(f, "Gerencie seus itens utilizando as opções ao lado.", 13, SUBTEXTO).pack(anchor="w")
        separador(f)
        cards = ctk.CTkFrame(f, fg_color="transparent")
        cards.pack(pady=10, anchor="w")
        for icone, titulo, desc, cor in [
            ("➕", "Cadastrar", "Adicione novos itens ao estoque", AZUL),
            ("🔍", "Consultar", "Visualize detalhes dos itens", VERDE),
            ("✏️", "Editar", "Modifique informações dos itens", LARANJA),
            ("📊", "Movimentar", "Adicione ou remova quantidades", VERMELHO),
        ]:
            c = ctk.CTkFrame(cards, fg_color=CARD, corner_radius=12, width=180)
            c.pack(side="left", padx=6, pady=4)
            label(c, f"{icone}  {titulo}", 14, cor, True).pack(padx=16, pady=(16,4), anchor="w")
            label(c, desc, 11, SUBTEXTO).pack(padx=16, pady=(0,16), anchor="w")

    # ═══════════════════════════════════════════
    #  ABA FORNECEDORES
    # ═══════════════════════════════════════════

    def _mostrar_sub_aba_fornecedores(self, key):
        """Mostra a sub-aba selecionada nos fornecedores"""
        for k, btn in self.btn_sub_fornecedores.items():
            btn.configure(fg_color=AZUL if k == key else "transparent",
                         text_color=TEXTO if k == key else SUBTEXTO)

        for w in self.content_fornecedores.winfo_children():
            w.destroy()

        f = self.content_fornecedores

        if key == "listar":
            self._forn_listar(f)
        elif key == "cadastrar":
            self._forn_cadastrar(f)
        elif key == "editar":
            self._forn_editar(f)

    # ═══════════════════════════════════════════
    #  FUNÇÕES DO ESTOQUE
    # ═══════════════════════════════════════════

    def _pg_cadastrar_item(self, f):
        """Cadastrar Item"""
        label(f, "Cadastrar Item", 20, TEXTO, True).pack(pady=(10,4), anchor="w")
        label(f, "Preencha os campos abaixo para cadastrar um novo item.", 12, SUBTEXTO).pack(anchor="w")
        separador(f)

        form = ctk.CTkFrame(f, fg_color=CARD, corner_radius=12)
        form.pack(pady=10, fill="x")

        e_nome = entry(form, "Nome do item")
        form_campo(form, "Nome *", e_nome)

        cb_tipo = combo(form, ["Camiseta", "Calça", "Calção", "Regata"])
        cb_tipo.set("Camiseta")
        form_campo(form, "Tipo *", cb_tipo)

        cb_modelo = combo(form, ["Manga Curta", "Manga Longa", "N/A"])
        cb_modelo.set("Manga Curta")
        form_campo(form, "Modelo", cb_modelo)

        def on_tipo_change(v):
            if v in ("Calça", "Calção"):
                cb_modelo.set("N/A"); cb_modelo.configure(state="disabled")
            else:
                cb_modelo.configure(state="normal")
                if cb_modelo.get() == "N/A": cb_modelo.set("Manga Curta")
        cb_tipo.configure(command=on_tipo_change)

        cb_tam = combo(form, ["P", "M", "G", "GG"]); cb_tam.set("M")
        form_campo(form, "Tamanho *", cb_tam)

        e_marca = entry(form, "Marca")
        form_campo(form, "Marca *", e_marca)

        e_qtd = entry(form, "0")
        form_campo(form, "Quantidade *", e_qtd)

        fornecedores_data = [{}]
        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT id, nome FROM fornecedor")
            fornecedores_data[0] = {r[1]: r[0] for r in cur.fetchall()}
            cur.close(); conn.close()

        nomes_f = list(fornecedores_data[0].keys()) or ["(sem fornecedores)"]
        cb_forn = combo(form, nomes_f); cb_forn.set(nomes_f[0])
        form_campo(form, "Fornecedor *", cb_forn)

        e_compra = entry(form, "0.00")
        form_campo(form, "Preço de Compra (R$) *", e_compra)

        e_venda = entry(form, "0.00")
        form_campo(form, "Preço de Venda (R$) *", e_venda)

        acao_frame = ctk.CTkFrame(form, fg_color="transparent")
        acao_frame.pack(fill="x", padx=24, pady=(8, 20))
        
        msg_item = label(acao_frame, "", 12, VERMELHO)
        msg_item.pack(anchor="w", pady=(0, 8))

        def salvar_item():
            nome  = e_nome.get().strip()
            tipo  = cb_tipo.get()
            modelo= cb_modelo.get()
            tam   = cb_tam.get()
            marca = e_marca.get().strip()
            erros = []
            if not nome:  erros.append("Nome obrigatório.")
            if not marca: erros.append("Marca obrigatória.")
            try: qtd = int(e_qtd.get()); assert qtd >= 0
            except: erros.append("Quantidade inválida (inteiro ≥ 0).")
            try: pc = float(e_compra.get()); assert pc >= 0
            except: erros.append("Preço de compra inválido.")
            try: pv = float(e_venda.get()); assert pv >= 0
            except: erros.append("Preço de venda inválido.")
            if erros:
                msg_item.configure(text="\n".join(erros), text_color=VERMELHO)
                return
            if pv < pc:
                msg_item.configure(text="Preço de venda deve ser ≥ preço de compra.", text_color=VERMELHO)
                return
            forn_nome = cb_forn.get()
            if forn_nome not in fornecedores_data[0]:
                msg_item.configure(text="Cadastre um fornecedor primeiro.", text_color=VERMELHO)
                return
            c = get_connection()
            if not c: return
            cur = c.cursor()
            cur.execute(
                "INSERT INTO itens (nome,tipo,modelo,tamanho,marca,quantidade,"
                "fornecedor,preco_compra,preco_venda,dia) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (nome, tipo, modelo, tam, marca, qtd, fornecedores_data[0][forn_nome],
                 pc, pv, datetime.datetime.now().strftime("%Y-%m-%d"))
            )
            c.commit()
            novo_id = cur.lastrowid
            cur.close(); c.close()
            msg_item.configure(text=f"✅ Item '{nome}' cadastrado! ID: {novo_id}", text_color=VERDE)
            for w in [e_nome, e_marca, e_qtd, e_compra, e_venda]: w.delete(0, "end")

        btn(acao_frame, "💾  Salvar Item", salvar_item, VERDE, "#15803D", 180).pack(anchor="w")

    def _pg_consultar_item(self, f):
        """Consultar Item"""
        label(f, "Consultar Itens", 20, TEXTO, True).pack(pady=(10,4), anchor="w")
        separador(f)

        topo = ctk.CTkFrame(f, fg_color="transparent")
        topo.pack(pady=6, fill="x")
        e_busca = entry(topo, "Buscar por ID...", 200)
        e_busca.pack(side="left")
        btn(topo, "🔍  Buscar", lambda: carregar_por_id(e_busca.get()), width=120).pack(side="left", padx=8)
        btn(topo, "↻  Atualizar", lambda: carregar_preview(), BORDA, "#475569", 140).pack(side="left")

        preview_frame = ctk.CTkFrame(f, fg_color=CARD, corner_radius=12)
        preview_frame.pack(pady=10, fill="x")
        
        ctk.CTkLabel(preview_frame, text="📋 Itens Cadastrados", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=TEXTO).pack(padx=20, pady=(14,8), anchor="w")
        
        header_frame = ctk.CTkFrame(preview_frame, fg_color=BORDA, corner_radius=6)
        header_frame.pack(fill="x", padx=20, pady=(0,4))
        ctk.CTkLabel(header_frame, text="ID", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=SUBTEXTO, width=60).pack(side="left", padx=2)
        ctk.CTkLabel(header_frame, text="Nome do Item", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=SUBTEXTO).pack(side="left", padx=10)
        
        preview_lista = ctk.CTkScrollableFrame(preview_frame, fg_color="transparent", height=300)
        preview_lista.pack(fill="x", padx=20, pady=(0,14))

        detalhe = ctk.CTkFrame(f, fg_color=CARD, corner_radius=12)
        msg_busca = ctk.CTkLabel(f, text="", font=ctk.CTkFont(size=12), text_color=SUBTEXTO)
        msg_busca.pack(pady=(4,0), anchor="w")

        def carregar_preview():
            for widget in preview_lista.winfo_children():
                widget.destroy()
            detalhe.pack_forget()
            
            conn = get_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, nome FROM itens ORDER BY id")
                rows = cur.fetchall()
                cur.close(); conn.close()
                
                if not rows:
                    ctk.CTkLabel(preview_lista, text="📭 Nenhum item cadastrado.", 
                                font=ctk.CTkFont(size=12), text_color=SUBTEXTO).pack(pady=20)
                    return
                
                for i, (id_item, nome_item) in enumerate(rows):
                    cor_fundo = CARD if i % 2 == 0 else BG
                    row_frame = ctk.CTkFrame(preview_lista, fg_color=cor_fundo, corner_radius=4, height=35)
                    row_frame.pack(fill="x", pady=1)
                    row_frame.pack_propagate(False)
                    
                    ctk.CTkLabel(row_frame, text=str(id_item), font=ctk.CTkFont(size=12),
                                text_color=TEXTO, width=60).pack(side="left", padx=2, pady=8)
                    ctk.CTkLabel(row_frame, text=nome_item, font=ctk.CTkFont(size=12),
                                text_color=TEXTO, anchor="w").pack(side="left", padx=10, pady=8)
                    ctk.CTkButton(row_frame, text="🔍 Ver", width=60, height=25,
                                fg_color=AZUL, hover_color=AZUL_ESC, corner_radius=4,
                                font=ctk.CTkFont(size=11),
                                command=lambda id_item=id_item: carregar_por_id(str(id_item))
                                ).pack(side="right", padx=8, pady=5)
            except Exception as e:
                print(f"Erro: {e}")

        def carregar_por_id(id_busca):
            for widget in detalhe.winfo_children():
                widget.destroy()
            detalhe.pack_forget()
            
            try:
                id_item = int(id_busca.strip())
            except ValueError:
                msg_busca.configure(text="⚠️ ID inválido.", text_color=LARANJA)
                return
            
            conn = get_connection()
            if not conn: return
            cur = conn.cursor()
            cur.execute("SELECT * FROM itens WHERE id = %s", (id_item,))
            row = cur.fetchone()
            cur.close(); conn.close()
            
            if not row:
                msg_busca.configure(text=f"❌ Item ID {id_item} não encontrado.", text_color=VERMELHO)
                return
            
            msg_busca.configure(text=f"✅ Item ID {id_item} encontrado!", text_color=VERDE)
            detalhe.pack(pady=10, fill="x")
            
            ctk.CTkLabel(detalhe, text=f"📦 Detalhes — {row[1]}", 
                        font=ctk.CTkFont(size=15, weight="bold"),
                        text_color=TEXTO).pack(padx=20, pady=(14,8), anchor="w")
            
            info = [
                ("ID", row[0]), ("Nome", row[1]), ("Tipo", row[2]),
                ("Modelo", row[3] if row[3] else "N/A"), ("Tamanho", row[4] if row[4] else "N/A"),
                ("Marca", row[5] if row[5] else "N/A"), ("Quantidade", row[6]),
                ("Fornecedor ID", row[7] if row[7] else "N/A"),
                ("Preço Compra", f"R$ {float(row[8]):.2f}"),
                ("Preço Venda", f"R$ {float(row[9]):.2f}"),
                ("Cadastrado em", str(row[10]) if row[10] else "N/A")
            ]
            
            grid = ctk.CTkFrame(detalhe, fg_color="transparent")
            grid.pack(padx=20, pady=(0,14), anchor="w")
            
            for col, (chave, valor) in enumerate(info):
                coluna, linha = col % 4, col // 4
                card = ctk.CTkFrame(grid, fg_color=BG, corner_radius=8, width=190, height=60)
                card.grid(row=linha, column=coluna, padx=4, pady=4)
                card.pack_propagate(False)
                ctk.CTkLabel(card, text=chave, font=ctk.CTkFont(size=10),
                            text_color=SUBTEXTO).pack(padx=12, pady=(8,0), anchor="w")
                ctk.CTkLabel(card, text=str(valor), font=ctk.CTkFont(size=13, weight="bold"),
                            text_color=TEXTO).pack(padx=12, pady=(0,8), anchor="w")

        carregar_preview()

    def _pg_editar_item(self, f):
        """Editar Item"""
        label(f, "Editar Item", 20, TEXTO, True).pack(pady=(10,4), anchor="w")
        separador(f)

        topo = ctk.CTkFrame(f, fg_color="transparent")
        topo.pack(pady=6, fill="x")
        
        ctk.CTkLabel(topo, text="Buscar por:", 
                    font=ctk.CTkFont(size=12),
                    text_color=SUBTEXTO).pack(side="left", padx=(0, 8))
        
        e_busca = entry(topo, "Digite o ID ou nome do item...", 300)
        e_busca.pack(side="left")
        
        btn(topo, "🔍  Buscar", lambda: buscar_item(e_busca.get()), AZUL, AZUL_ESC, 140).pack(side="left", padx=8)
        btn(topo, "↻  Mostrar Todos", lambda: carregar_preview_edicao(), BORDA, "#475569", 140).pack(side="left")
        
        msg_busca = ctk.CTkLabel(topo, text="", font=ctk.CTkFont(size=12), text_color=SUBTEXTO)
        msg_busca.pack(side="left", padx=12)

        preview_frame = ctk.CTkFrame(f, fg_color=CARD, corner_radius=12)
        preview_frame.pack(pady=10, fill="x")
        
        ctk.CTkLabel(preview_frame, text="📋 Selecione um item para editar", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=TEXTO).pack(padx=20, pady=(14,8), anchor="w")
        
        header_frame = ctk.CTkFrame(preview_frame, fg_color=BORDA, corner_radius=6)
        header_frame.pack(fill="x", padx=20, pady=(0,4))
        ctk.CTkLabel(header_frame, text="ID", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=SUBTEXTO, width=60).pack(side="left", padx=2)
        ctk.CTkLabel(header_frame, text="Nome do Item", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=SUBTEXTO).pack(side="left", padx=10)
        ctk.CTkLabel(header_frame, text="Tipo", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=SUBTEXTO, width=100).pack(side="left", padx=2)
        
        preview_lista = ctk.CTkScrollableFrame(preview_frame, fg_color="transparent", height=200)
        preview_lista.pack(fill="x", padx=20, pady=(0,14))

        form = ctk.CTkFrame(f, fg_color=CARD, corner_radius=12)
        campos_ws = {}

        def carregar_preview_edicao(filtro=None):
            for widget in preview_lista.winfo_children():
                widget.destroy()
            
            conn = get_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                
                if filtro:
                    try:
                        id_busca = int(filtro)
                        cur.execute("SELECT id, nome, tipo FROM itens WHERE id = %s", (id_busca,))
                    except ValueError:
                        cur.execute("SELECT id, nome, tipo FROM itens WHERE nome LIKE %s ORDER BY id", 
                                   (f"%{filtro}%",))
                else:
                    cur.execute("SELECT id, nome, tipo FROM itens ORDER BY id")
                
                rows = cur.fetchall()
                cur.close()
                conn.close()
                
                if not rows:
                    ctk.CTkLabel(preview_lista, text="📭 Nenhum item encontrado.", 
                                font=ctk.CTkFont(size=12), text_color=SUBTEXTO).pack(pady=20)
                    return
                
                for i, (id_item, nome_item, tipo_item) in enumerate(rows):
                    cor_fundo = CARD if i % 2 == 0 else BG
                    row_frame = ctk.CTkFrame(preview_lista, fg_color=cor_fundo, corner_radius=4, height=35)
                    row_frame.pack(fill="x", pady=1)
                    row_frame.pack_propagate(False)
                    
                    ctk.CTkLabel(row_frame, text=str(id_item), font=ctk.CTkFont(size=12),
                                text_color=TEXTO, width=60).pack(side="left", padx=2, pady=8)
                    ctk.CTkLabel(row_frame, text=nome_item, font=ctk.CTkFont(size=12),
                                text_color=TEXTO, anchor="w").pack(side="left", padx=10, pady=8)
                    ctk.CTkLabel(row_frame, text=tipo_item, font=ctk.CTkFont(size=11),
                                text_color=SUBTEXTO, width=100).pack(side="left", padx=2, pady=8)
                    ctk.CTkButton(row_frame, text="✏️ Editar", width=70, height=25,
                                fg_color=VERDE, hover_color="#15803D", corner_radius=4,
                                font=ctk.CTkFont(size=11),
                                command=lambda id_item=id_item: carregar_item_para_editar(id_item)
                                ).pack(side="right", padx=8, pady=5)
                    
            except Exception as e:
                print(f"Erro: {e}")

        def buscar_item(texto_busca):
            texto_busca = texto_busca.strip()
            if not texto_busca:
                msg_busca.configure(text="⚠️ Digite um ID ou nome para buscar.", text_color=LARANJA)
                return
            form.pack_forget()
            msg_busca.configure(text=f"🔍 Buscando por: {texto_busca}", text_color=SUBTEXTO)
            carregar_preview_edicao(texto_busca)

        def carregar_item_para_editar(id_item):
            conn = get_connection()
            if not conn: return
            cur = conn.cursor()
            cur.execute("SELECT * FROM itens WHERE id=%s", (id_item,))
            row = cur.fetchone()
            cur.close()
            conn.close()
            
            if not row:
                msg_busca.configure(text="❌ Item não encontrado.", text_color=VERMELHO)
                return
            
            msg_busca.configure(text=f"✅ Editando: {row[1]} (ID: {id_item})", text_color=VERDE)
            
            for w in form.winfo_children():
                w.destroy()
            campos_ws.clear()
            form.pack(pady=10, fill="x")
            
            ctk.CTkLabel(form, text=f"Editando: {row[1]}", font=ctk.CTkFont(size=16, weight="bold"),
                        text_color=TEXTO).pack(padx=24, pady=(14,8), anchor="w")

            for campo, rotulo, valor in [
                ("nome","Nome",row[1]), ("tipo","Tipo",row[2]),
                ("modelo","Modelo",row[3]), ("tamanho","Tamanho",row[4]),
                ("marca","Marca",row[5]), ("preco_compra","Preço Compra",str(row[8])),
                ("preco_venda","Preço Venda",str(row[9])),
            ]:
                r = ctk.CTkFrame(form, fg_color="transparent")
                r.pack(fill="x", padx=24, pady=5)
                label(r, rotulo, 12, SUBTEXTO).pack(anchor="w")
                
                if campo == "tipo":
                    w = combo(r, ["Camiseta","Calça","Calção","Regata"]); w.set(valor)
                elif campo == "modelo":
                    w = combo(r, ["Manga Curta","Manga Longa","N/A"]); w.set(valor if valor else "N/A")
                elif campo == "tamanho":
                    w = combo(r, ["P","M","G","GG"]); w.set(valor if valor else "M")
                else:
                    w = entry(r); w.insert(0, valor)
                w.pack(anchor="w", pady=(2,0))
                campos_ws[campo] = w

            acao_frame = ctk.CTkFrame(form, fg_color="transparent")
            acao_frame.pack(fill="x", padx=24, pady=(8, 20))
            
            msg_form = ctk.CTkLabel(acao_frame, text="", font=ctk.CTkFont(size=12), text_color=VERMELHO)
            msg_form.pack(anchor="w", pady=(0, 8))

            def salvar_item():
                try:
                    novo_pc = float(campos_ws["preco_compra"].get())
                    novo_pv = float(campos_ws["preco_venda"].get())
                except:
                    msg_form.configure(text="Preços inválidos."); return
                
                novo_nome  = campos_ws["nome"].get().strip()
                novo_tipo  = campos_ws["tipo"].get()
                novo_modelo= campos_ws["modelo"].get()
                novo_tam   = campos_ws["tamanho"].get()
                novo_marca = campos_ws["marca"].get().strip()
                
                erros = []
                if not novo_nome: erros.append("Nome vazio.")
                if not novo_marca: erros.append("Marca vazia.")
                if novo_pc < 0: erros.append("Preço compra inválido.")
                if novo_pv < novo_pc: erros.append("Preço venda < preço compra.")
                if erros:
                    msg_form.configure(text="\n".join(erros)); return
                
                c = get_connection()
                if not c: return
                cur2 = c.cursor()
                cur2.execute(
                    "UPDATE itens SET nome=%s,tipo=%s,modelo=%s,tamanho=%s,marca=%s,"
                    "preco_compra=%s,preco_venda=%s WHERE id=%s",
                    (novo_nome,novo_tipo,novo_modelo,novo_tam,novo_marca,novo_pc,novo_pv,id_item))
                c.commit(); cur2.close(); c.close()
                msg_form.configure(text="✅ Item atualizado com sucesso!", text_color=VERDE)
                carregar_preview_edicao()
                msg_busca.configure(text="")

            ctk.CTkButton(acao_frame, text="💾  Salvar Alterações", command=salvar_item,
                         fg_color=VERDE, hover_color="#15803D", corner_radius=8,
                         width=200, font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w")

        carregar_preview_edicao()

    def _pg_movimentar_item(self, f, adicionar):
        """Adicionar/Remover Estoque"""
        titulo = "Adicionar ao Estoque" if adicionar else "Remover do Estoque"
        cor_btn = VERDE if adicionar else VERMELHO
        hover_btn = "#15803D" if adicionar else "#B91C1C"
        
        label(f, titulo, 20, TEXTO, True).pack(pady=(10,4), anchor="w")
        separador(f)

        frame = ctk.CTkFrame(f, fg_color=CARD, corner_radius=12)
        frame.pack(pady=10, fill="x")

        conn = get_connection(); itens_map = {}
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT id, nome, quantidade FROM itens")
            itens_map = {f"{r[1]} (ID:{r[0]}, Estoque:{r[2]})": (r[0], r[2]) for r in cur.fetchall()}
            cur.close(); conn.close()

        opcoes = list(itens_map.keys()) or ["(sem itens)"]
        label(frame, "Selecione o item:", 12, SUBTEXTO).pack(padx=20, pady=(14,4), anchor="w")
        cb_item = combo(frame, opcoes, 460); cb_item.set(opcoes[0]); cb_item.pack(padx=20, anchor="w")
        label(frame, "Quantidade:", 12, SUBTEXTO).pack(padx=20, pady=(12,4), anchor="w")
        e_qtd = entry(frame, "1", 180); e_qtd.pack(padx=20, anchor="w")

        msg = label(frame, "", 12, VERMELHO)
        msg.pack(padx=20, pady=(4,0), anchor="w")

        def executar():
            chave = cb_item.get()
            if chave not in itens_map:
                msg.configure(text="Selecione um item válido.", text_color=VERMELHO); return
            id_item, estoque_atual = itens_map[chave]
            try: qtd = int(e_qtd.get()); assert qtd > 0
            except: msg.configure(text="Quantidade inteira positiva.", text_color=VERMELHO); return
            if not adicionar and qtd > estoque_atual:
                msg.configure(text=f"Estoque insuficiente ({estoque_atual} un).", text_color=VERMELHO); return
            c = get_connection()
            if not c: return
            cur = c.cursor()
            cur.execute("UPDATE itens SET quantidade=quantidade+%s WHERE id=%s",
                        (qtd if adicionar else -qtd, id_item))
            c.commit(); cur.close(); c.close()
            msg.configure(text=f"✅ {qtd} unidade(s) {'adicionadas' if adicionar else 'removidas'}!", text_color=VERDE)

        btn(frame, f"{'➕' if adicionar else '➖'}  Confirmar", executar, cor_btn, hover_btn, 180).pack(padx=20, pady=(8,20), anchor="w")

    # ═══════════════════════════════════════════
    #  FUNÇÕES DOS FORNECEDORES
    # ═══════════════════════════════════════════

    def _forn_listar(self, pai):
        conn = get_connection()
        if not conn: return
        cur = conn.cursor()
        cur.execute("SELECT * FROM fornecedor")
        rows = cur.fetchall(); cur.close(); conn.close()

        tabela = ctk.CTkScrollableFrame(pai, fg_color=CARD, corner_radius=12, height=360)
        tabela.pack(fill="x", pady=10)
        cabs  = ["ID","Nome","CPF","CNPJ","Endereço","Telefone","E-mail"]
        largs = [40, 160, 110, 130, 180, 120, 180]

        hdr = ctk.CTkFrame(tabela, fg_color=BORDA, corner_radius=6)
        hdr.pack(fill="x", padx=8, pady=(8,2))
        for c, l in zip(cabs, largs):
            lbl = ctk.CTkLabel(hdr, text=c, font=ctk.CTkFont(size=11, weight="bold"),
                             text_color=SUBTEXTO, width=l, anchor="center")
            lbl.pack(side="left", padx=2)

        if not rows:
            ctk.CTkLabel(tabela, text="Nenhum fornecedor cadastrado.", 
                        font=ctk.CTkFont(size=13), text_color=SUBTEXTO).pack(pady=20)
            return
            
        for i, r in enumerate(rows):
            cor_fundo = CARD if i%2==0 else BG
            row = ctk.CTkFrame(tabela, fg_color=cor_fundo, corner_radius=4, height=34)
            row.pack(fill="x", pady=1)
            row.pack_propagate(False)
            for v, l in zip(r, largs):
                lbl = ctk.CTkLabel(row, text=str(v), font=ctk.CTkFont(size=12),
                                 text_color=TEXTO, width=l, anchor="center")
                lbl.pack(side="left", padx=2)

    def _forn_cadastrar(self, pai):
        form = ctk.CTkFrame(pai, fg_color=CARD, corner_radius=12)
        form.pack(fill="x", pady=10)

        ws = {}
        for key, rot in [("nome","Nome *"),("cpf","CPF (11 dígitos) *"),
                         ("cnpj","CNPJ (14 dígitos) *"),("endereco","Endereço *"),
                         ("telefone","Telefone (10+ dígitos) *"),("email","E-mail *")]:
            e = entry(form)
            form_campo(form, rot, e)
            ws[key] = e

        acao_frame = ctk.CTkFrame(form, fg_color="transparent")
        acao_frame.pack(fill="x", padx=24, pady=(12, 20))
        
        msg = label(acao_frame, "", 12, VERMELHO)
        msg.pack(anchor="w", pady=(0, 8))

        def salvar_forn():
            nome=ws["nome"].get().strip(); cpf=ws["cpf"].get().strip()
            cnpj=ws["cnpj"].get().strip(); endereco=ws["endereco"].get().strip()
            telefone=ws["telefone"].get().strip(); email=ws["email"].get().strip()
            erros=[]
            if not nome: erros.append("Nome obrigatório.")
            if not cpf.isdigit() or len(cpf)!=11: erros.append("CPF: 11 dígitos numéricos.")
            if not cnpj.isdigit() or len(cnpj)!=14: erros.append("CNPJ: 14 dígitos numéricos.")
            if not endereco: erros.append("Endereço obrigatório.")
            if not telefone.isdigit() or len(telefone)<10: erros.append("Telefone: mín. 10 dígitos.")
            if "@" not in email or "." not in email: erros.append("E-mail inválido.")
            if erros:
                msg.configure(text="\n".join(erros), text_color=VERMELHO); return
            conn=get_connection()
            if not conn: return
            cur=conn.cursor()
            cur.execute("SELECT id FROM fornecedor WHERE cpf=%s",(cpf,))
            if cur.fetchone():
                msg.configure(text="CPF já cadastrado.",text_color=VERMELHO)
                cur.close();conn.close();return
            cur.execute("SELECT id FROM fornecedor WHERE cnpj=%s",(cnpj,))
            if cur.fetchone():
                msg.configure(text="CNPJ já cadastrado.",text_color=VERMELHO)
                cur.close();conn.close();return
            cur.execute(
                "INSERT INTO fornecedor (nome,cpf,cnpj,endereco,telefone,email) VALUES(%s,%s,%s,%s,%s,%s)",
                (nome,cpf,cnpj,endereco,telefone,email))
            conn.commit(); cur.close(); conn.close()
            msg.configure(text=f"✅ Fornecedor '{nome}' cadastrado!", text_color=VERDE)
            for w in ws.values(): w.delete(0,"end")

        btn(acao_frame, "💾  Salvar Fornecedor", salvar_forn, VERDE, "#15803D", 200).pack(anchor="w")

    def _forn_editar(self, pai):
        preview_frame = ctk.CTkFrame(pai, fg_color=CARD, corner_radius=12)
        preview_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(preview_frame, text="📋 Selecione um fornecedor para editar", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=TEXTO).pack(padx=20, pady=(14,8), anchor="w")
        
        header_frame = ctk.CTkFrame(preview_frame, fg_color=BORDA, corner_radius=6)
        header_frame.pack(fill="x", padx=20, pady=(0,4))
        ctk.CTkLabel(header_frame, text="ID", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=SUBTEXTO, width=60).pack(side="left", padx=2)
        ctk.CTkLabel(header_frame, text="Nome do Fornecedor", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=SUBTEXTO).pack(side="left", padx=10)
        
        preview_lista = ctk.CTkScrollableFrame(preview_frame, fg_color="transparent", height=180)
        preview_lista.pack(fill="x", padx=20, pady=(0,14))

        topo = ctk.CTkFrame(pai, fg_color="transparent")
        topo.pack(pady=8, fill="x")
        
        ctk.CTkLabel(topo, text="Buscar fornecedor:", 
                    font=ctk.CTkFont(size=12),
                    text_color=SUBTEXTO).pack(side="left", padx=(0, 8))
        
        e_busca = entry(topo, "Digite o ID ou nome do fornecedor...", 250)
        e_busca.pack(side="left")
        
        btn(topo, "🔍  Buscar", lambda: buscar_fornecedor(e_busca.get()), AZUL, AZUL_ESC, 140).pack(side="left", padx=8)
        btn(topo, "↻  Mostrar Todos", lambda: carregar_preview_edicao(), BORDA, "#475569", 140).pack(side="left")
        
        msg_topo = ctk.CTkLabel(topo, text="", font=ctk.CTkFont(size=12), text_color=SUBTEXTO)
        msg_topo.pack(side="left", padx=12)

        form = ctk.CTkFrame(pai, fg_color=CARD, corner_radius=12)
        campos_ws = {}

        def carregar_preview_edicao(filtro=None):
            for widget in preview_lista.winfo_children():
                widget.destroy()
            
            conn = get_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                
                if filtro:
                    try:
                        id_busca = int(filtro)
                        cur.execute("SELECT id, nome FROM fornecedor WHERE id = %s", (id_busca,))
                    except ValueError:
                        cur.execute("SELECT id, nome FROM fornecedor WHERE nome LIKE %s ORDER BY id", 
                                   (f"%{filtro}%",))
                else:
                    cur.execute("SELECT id, nome FROM fornecedor ORDER BY id")
                
                rows = cur.fetchall()
                cur.close()
                conn.close()
                
                if not rows:
                    ctk.CTkLabel(preview_lista, text="📭 Nenhum fornecedor encontrado.", 
                                font=ctk.CTkFont(size=12), text_color=SUBTEXTO).pack(pady=20)
                    return
                
                for i, (id_forn, nome_forn) in enumerate(rows):
                    cor_fundo = CARD if i % 2 == 0 else BG
                    row_frame = ctk.CTkFrame(preview_lista, fg_color=cor_fundo, corner_radius=4, height=35)
                    row_frame.pack(fill="x", pady=1)
                    row_frame.pack_propagate(False)
                    
                    ctk.CTkLabel(row_frame, text=str(id_forn), font=ctk.CTkFont(size=12),
                                text_color=TEXTO, width=60).pack(side="left", padx=2, pady=8)
                    ctk.CTkLabel(row_frame, text=nome_forn, font=ctk.CTkFont(size=12),
                                text_color=TEXTO, anchor="w").pack(side="left", padx=10, pady=8)
                    ctk.CTkButton(row_frame, text="✏️ Editar", width=70, height=25,
                                fg_color=VERDE, hover_color="#15803D", corner_radius=4,
                                font=ctk.CTkFont(size=11),
                                command=lambda id_forn=id_forn: carregar_forn_para_editar(id_forn)
                                ).pack(side="right", padx=8, pady=5)
                    
            except Exception as e:
                print(f"Erro: {e}")

        def buscar_fornecedor(texto_busca):
            texto_busca = texto_busca.strip()
            if not texto_busca:
                msg_topo.configure(text="⚠️ Digite um ID ou nome para buscar.", text_color=LARANJA)
                return
            form.pack_forget()
            msg_topo.configure(text=f"🔍 Buscando por: {texto_busca}", text_color=SUBTEXTO)
            carregar_preview_edicao(texto_busca)

        def carregar_forn_para_editar(fid):
            conn = get_connection()
            if not conn: return
            
            cur = conn.cursor()
            cur.execute("SELECT * FROM fornecedor WHERE id=%s", (fid,))
            r = cur.fetchone()
            cur.close()
            conn.close()
            
            if not r:
                msg_topo.configure(text=f"❌ Fornecedor com ID {fid} não encontrado.", text_color=VERMELHO)
                return
            
            msg_topo.configure(text=f"✅ Editando: {r[1]} (ID: {fid})", text_color=VERDE)
            
            for w in form.winfo_children():
                w.destroy()
            campos_ws.clear()
            form.pack(fill="x", pady=10)
            
            ctk.CTkLabel(form, text=f"Editando: {r[1]}", font=ctk.CTkFont(size=16, weight="bold"),
                        text_color=TEXTO).pack(padx=24, pady=(14,8), anchor="w")

            for key, rot, val in [
                ("nome","Nome",r[1]), ("cpf","CPF",r[2]), ("cnpj","CNPJ",r[3]),
                ("endereco","Endereço",r[4]), ("telefone","Telefone",r[5]), ("email","E-mail",r[6])
            ]:
                row_frame = ctk.CTkFrame(form, fg_color="transparent")
                row_frame.pack(fill="x", padx=24, pady=5)
                label(row_frame, rot, 12, SUBTEXTO).pack(anchor="w")
                e = entry(row_frame)
                e.insert(0, val if val else "")
                e.pack(anchor="w", pady=(2,0))
                campos_ws[key] = e

            acao_frame = ctk.CTkFrame(form, fg_color="transparent")
            acao_frame.pack(fill="x", padx=24, pady=(8, 20))
            
            msg_form = ctk.CTkLabel(acao_frame, text="", font=ctk.CTkFont(size=12), text_color=VERMELHO)
            msg_form.pack(anchor="w", pady=(0, 8))

            def salvar_edicao():
                nome = campos_ws["nome"].get().strip()
                cpf = campos_ws["cpf"].get().strip()
                cnpj = campos_ws["cnpj"].get().strip()
                endereco = campos_ws["endereco"].get().strip()
                telefone = campos_ws["telefone"].get().strip()
                email = campos_ws["email"].get().strip()
                
                erros = []
                if not nome: erros.append("Nome vazio.")
                if not cpf.isdigit() or len(cpf)!=11: erros.append("CPF inválido (11 dígitos).")
                if not cnpj.isdigit() or len(cnpj)!=14: erros.append("CNPJ inválido (14 dígitos).")
                if not endereco: erros.append("Endereço vazio.")
                if not telefone.isdigit() or len(telefone)<10: erros.append("Telefone inválido (mín. 10 dígitos).")
                if "@" not in email or "." not in email: erros.append("E-mail inválido.")
                
                if erros:
                    msg_form.configure(text="\n".join(erros), text_color=VERMELHO)
                    return
                
                c = get_connection()
                if not c: return
                cur2 = c.cursor()
                cur2.execute(
                    "UPDATE fornecedor SET nome=%s,cpf=%s,cnpj=%s,endereco=%s,telefone=%s,email=%s WHERE id=%s",
                    (nome, cpf, cnpj, endereco, telefone, email, fid))
                c.commit()
                cur2.close()
                c.close()
                
                msg_form.configure(text="✅ Fornecedor atualizado com sucesso!", text_color=VERDE)
                carregar_preview_edicao()
                e_busca.delete(0, "end")
                msg_topo.configure(text="")

            ctk.CTkButton(acao_frame, text="💾  Salvar Alterações", command=salvar_edicao,
                         fg_color=VERDE, hover_color="#15803D", corner_radius=8,
                         width=200, font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w")

        carregar_preview_edicao()

    # ═══════════════════════════════════════════
    #  CALCULADORA DE PRECIFICAÇÃO + PESQUISA
    # ═══════════════════════════════════════════

    def _pg_calculadora(self, f):
        """Calculadora de Precificação + Pesquisa de Itens"""
        for w in f.winfo_children():
            w.destroy()

        # Container principal com duas colunas
        container = ctk.CTkFrame(f, fg_color="transparent")
        container.pack(fill="both", expand=True)

        # Coluna esquerda - Calculadora
        col_esq = ctk.CTkFrame(container, fg_color="transparent")
        col_esq.pack(side="left", fill="both", expand=True, padx=(0,10))

        # Coluna direita - Pesquisa
        col_dir = ctk.CTkFrame(container, fg_color="transparent")
        col_dir.pack(side="right", fill="both", expand=True, padx=(10,0))

        # ═══════════════════════════════════════
        #  COLUNA ESQUERDA - CALCULADORA
        # ═══════════════════════════════════════
        label(col_esq, "Calculadora de Precificação", 18, TEXTO, True).pack(pady=(10,4), anchor="w")
        label(col_esq, "Calcule o preço de venda ideal.", 11, SUBTEXTO).pack(anchor="w")
        separador(col_esq)

        main_frame = ctk.CTkFrame(col_esq, fg_color=CARD, corner_radius=12)
        main_frame.pack(pady=10, fill="x")

        # Seção: Custos do Produto
        ctk.CTkLabel(main_frame, text="📦  CUSTOS DO PRODUTO", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=AZUL).pack(padx=20, pady=(12,4), anchor="w")

        campos_custos = {}
        for campo, rotulo in [
            ("preco_custo", "Preço de custo da peça"),
            ("frete", "Frete de compra"),
        ]:
            r = ctk.CTkFrame(main_frame, fg_color="transparent")
            r.pack(fill="x", padx=20, pady=3)
            label(r, rotulo, 10, SUBTEXTO).pack(anchor="w")
            e = entry(r, "0.00", 200)
            e.pack(anchor="w", pady=(1,0))
            campos_custos[campo] = e

        ctk.CTkLabel(main_frame, text="🏷️  Etiquetas", font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=SUBTEXTO).pack(padx=20, pady=(6,4), anchor="w")

        for campo, rotulo in [
            ("etiq_interna", "Etiqueta interna"),
            ("etiq_externa", "Etiqueta externa"),
            ("etiq_termo", "Etiqueta termocolante"),
        ]:
            r = ctk.CTkFrame(main_frame, fg_color="transparent")
            r.pack(fill="x", padx=20, pady=3)
            label(r, rotulo, 10, SUBTEXTO).pack(anchor="w")
            e = entry(r, "0.00", 200)
            e.pack(anchor="w", pady=(1,0))
            campos_custos[campo] = e

        ctk.CTkLabel(main_frame, text="🛍️  Embalagem", font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=SUBTEXTO).pack(padx=20, pady=(6,4), anchor="w")

        for campo, rotulo in [
            ("embalagem", "Embalagem"),
            ("sacola", "Sacola"),
            ("outros", "Outros custos"),
        ]:
            r = ctk.CTkFrame(main_frame, fg_color="transparent")
            r.pack(fill="x", padx=20, pady=3)
            label(r, rotulo, 10, SUBTEXTO).pack(anchor="w")
            e = entry(r, "0.00", 200)
            e.pack(anchor="w", pady=(1,0))
            campos_custos[campo] = e

        separador(main_frame)

        # Seção: Percentuais
        ctk.CTkLabel(main_frame, text="📊  PERCENTUAIS", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=AZUL).pack(padx=20, pady=(4,4), anchor="w")

        campos_pcts = {}
        for campo, rotulo in [
            ("impostos", "Impostos (%)"),
            ("cartao", "Taxa de cartão (%)"),
            ("comissao", "Comissão de vendedor (%)"),
            ("lucro", "Percentual de lucro desejado (%)"),
        ]:
            r = ctk.CTkFrame(main_frame, fg_color="transparent")
            r.pack(fill="x", padx=20, pady=3)
            label(r, rotulo, 10, SUBTEXTO).pack(anchor="w")
            e = entry(r, "0", 200)
            e.pack(anchor="w", pady=(1,0))
            campos_pcts[campo] = e

        # Botões
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(12,8))

        btn(btn_frame, "🧮  CALCULAR", lambda: self._calcular_precificacao(campos_custos, campos_pcts, resultado_frame), 
            VERDE, "#15803D", 160).pack(side="left", padx=(0,6))
        btn(btn_frame, "↺  Limpar", lambda: self._limpar_calculadora(campos_custos, campos_pcts, resultado_frame), 
            BORDA, "#475569", 100).pack(side="left")

        # Frame de resultado
        resultado_frame = ctk.CTkFrame(col_esq, fg_color=CARD, corner_radius=12)
        resultado_frame.pack(pady=10, fill="x")

        # ═══════════════════════════════════════
        #  COLUNA DIREITA - PESQUISA DE ITENS
        # ═══════════════════════════════════════
        label(col_dir, "Pesquisar Itens", 18, TEXTO, True).pack(pady=(10,4), anchor="w")
        label(col_dir, "Busque por ID ou nome do item.", 11, SUBTEXTO).pack(anchor="w")
        separador(col_dir)

        # Campo de busca
        busca_frame = ctk.CTkFrame(col_dir, fg_color="transparent")
        busca_frame.pack(fill="x", pady=(0,8))

        e_busca = entry(busca_frame, "Digite ID ou nome do item...", 220)
        e_busca.pack(side="left")

        btn(busca_frame, "🔍", lambda: pesquisar_itens(e_busca.get()), AZUL, AZUL_ESC, 40).pack(side="left", padx=4)

        # Frame de preview
        preview_frame = ctk.CTkFrame(col_dir, fg_color=CARD, corner_radius=12)
        preview_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(preview_frame, text="📋 Itens Encontrados", 
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color=TEXTO).pack(padx=16, pady=(12,6), anchor="w")

        # Header
        header_frame = ctk.CTkFrame(preview_frame, fg_color=BORDA, corner_radius=4)
        header_frame.pack(fill="x", padx=16, pady=(0,4))

        headers = [
            ("ID", 40),
            ("Nome", 120),
            ("Compra", 80),
            ("Qtd", 50),
        ]

        for texto, largura in headers:
            ctk.CTkLabel(header_frame, text=texto, font=ctk.CTkFont(size=10, weight="bold"),
                        text_color=SUBTEXTO, width=largura).pack(side="left", padx=1)

        # Lista de itens
        lista_itens = ctk.CTkScrollableFrame(preview_frame, fg_color="transparent", height=350)
        lista_itens.pack(fill="both", expand=True, padx=16, pady=(0,12))

        msg_status = ctk.CTkLabel(col_dir, text="", font=ctk.CTkFont(size=11), text_color=SUBTEXTO)
        msg_status.pack(pady=(4,0), anchor="w")

        def pesquisar_itens(filtro=""):
            """Pesquisa itens por ID ou nome"""
            for widget in lista_itens.winfo_children():
                widget.destroy()

            filtro = filtro.strip()

            conn = get_connection()
            if not conn:
                ctk.CTkLabel(lista_itens, text="❌ Erro de conexão.", 
                            font=ctk.CTkFont(size=11), text_color=VERMELHO).pack(pady=10)
                return

            try:
                cur = conn.cursor()

                if filtro:
                    try:
                        id_busca = int(filtro)
                        cur.execute("SELECT id, nome, preco_compra, quantidade FROM itens WHERE id = %s", (id_busca,))
                    except ValueError:
                        cur.execute("SELECT id, nome, preco_compra, quantidade FROM itens WHERE nome LIKE %s ORDER BY id", 
                                   (f"%{filtro}%",))
                else:
                    cur.execute("SELECT id, nome, preco_compra, quantidade FROM itens ORDER BY id")

                rows = cur.fetchall()
                cur.close()
                conn.close()

                if not rows:
                    ctk.CTkLabel(lista_itens, text="📭 Nenhum item encontrado.", 
                                font=ctk.CTkFont(size=11), text_color=SUBTEXTO).pack(pady=10)
                    msg_status.configure(text="")
                    return

                msg_status.configure(text=f"✅ {len(rows)} item(ns) encontrado(s)")

                for i, (id_item, nome_item, preco_compra, quantidade) in enumerate(rows):
                    cor_fundo = CARD if i % 2 == 0 else BG
                    row_frame = ctk.CTkFrame(lista_itens, fg_color=cor_fundo, corner_radius=4, height=30)
                    row_frame.pack(fill="x", pady=1)
                    row_frame.pack_propagate(False)

                    ctk.CTkLabel(row_frame, text=str(id_item), 
                                font=ctk.CTkFont(size=11),
                                text_color=TEXTO, width=40).pack(side="left", padx=2, pady=6)
                    ctk.CTkLabel(row_frame, text=nome_item, 
                                font=ctk.CTkFont(size=11),
                                text_color=TEXTO, anchor="w", width=120).pack(side="left", padx=2, pady=6)
                    ctk.CTkLabel(row_frame, text=f"R$ {float(preco_compra):.2f}".replace(".", ","), 
                                font=ctk.CTkFont(size=11, weight="bold"),
                                text_color=VERDE, width=80).pack(side="left", padx=2, pady=6)
                    ctk.CTkLabel(row_frame, text=str(quantidade), 
                                font=ctk.CTkFont(size=11, weight="bold"),
                                text_color=AZUL if quantidade > 0 else VERMELHO, width=50).pack(side="left", padx=2, pady=6)

            except Exception as e:
                print(f"Erro na pesquisa: {e}")
                ctk.CTkLabel(lista_itens, text=f"❌ Erro: {str(e)}", 
                            font=ctk.CTkFont(size=11), text_color=VERMELHO).pack(pady=10)

        # Carregar todos os itens inicialmente
        pesquisar_itens()

    def _calcular_precificacao(self, custos, pcts, resultado_frame):
        """Realiza o cálculo de precificação"""
        for w in resultado_frame.winfo_children():
            w.destroy()

        try:
            valores = {}
            for k, e in custos.items():
                try:
                    valores[k] = float(e.get().replace(",", "."))
                except:
                    valores[k] = 0.0
            
            pct_valores = {}
            for k, e in pcts.items():
                try:
                    pct_valores[k] = float(e.get().replace(",", "."))
                except:
                    pct_valores[k] = 0.0

            custo_total = sum(valores.values())
            total_pct = sum(pct_valores.values()) / 100

            if total_pct >= 1.0:
                ctk.CTkLabel(resultado_frame, text="❌ A soma dos percentuais é ≥ 100%!", 
                            font=ctk.CTkFont(size=11), text_color=VERMELHO).pack(padx=20, pady=10)
                return

            if custo_total <= 0:
                ctk.CTkLabel(resultado_frame, text="⚠️ Informe ao menos o preço de custo.", 
                            font=ctk.CTkFont(size=11), text_color=LARANJA).pack(padx=20, pady=10)
                return

            preco_venda = custo_total / (1 - total_pct)
            preco_arredondado = arredondar_preco(preco_venda)

            lucro_rs = preco_arredondado - custo_total
            lucro_pct_real = (lucro_rs / preco_arredondado * 100) if preco_arredondado > 0 else 0
            markup = (preco_arredondado / custo_total) if custo_total > 0 else 0

            ctk.CTkLabel(resultado_frame, text="RESULTADO", 
                        font=ctk.CTkFont(size=13, weight="bold"),
                        text_color=AZUL).pack(padx=20, pady=(10,6), anchor="w")

            ctk.CTkLabel(resultado_frame, text=f"Custo Total: R$ {custo_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 
                        font=ctk.CTkFont(size=12, weight="bold"),
                        text_color=TEXTO).pack(padx=20, anchor="w")

            ctk.CTkLabel(resultado_frame, text=f"Preço Calculado: R$ {preco_venda:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 
                        font=ctk.CTkFont(size=11),
                        text_color=SUBTEXTO).pack(padx=20, anchor="w")

            destaque = ctk.CTkFrame(resultado_frame, fg_color=AZUL, corner_radius=8)
            destaque.pack(fill="x", padx=20, pady=8)
            ctk.CTkLabel(destaque, text="💰  PREÇO SUGERIDO", 
                        font=ctk.CTkFont(size=10, weight="bold"),
                        text_color=TEXTO).pack(pady=(6,2))
            ctk.CTkLabel(destaque, text=f"R$ {preco_arredondado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 
                        font=ctk.CTkFont(size=20, weight="bold"),
                        text_color=TEXTO).pack(pady=(0,6))

            ind_frame = ctk.CTkFrame(resultado_frame, fg_color="transparent")
            ind_frame.pack(fill="x", padx=20, pady=(0,10))

            for titulo, valor, cor in [
                ("Lucro R$", f"R$ {lucro_rs:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), VERDE if lucro_rs > 0 else VERMELHO),
                ("Lucro %", f"{lucro_pct_real:.1f}%".replace(".", ","), VERDE if lucro_rs > 0 else VERMELHO),
                ("Markup", f"{markup:.2f}x".replace(".", ","), VERDE if markup >= 1 else VERMELHO),
            ]:
                card = ctk.CTkFrame(ind_frame, fg_color=BG, corner_radius=6)
                card.pack(side="left", fill="both", expand=True, padx=2)
                ctk.CTkLabel(card, text=titulo, font=ctk.CTkFont(size=8),
                            text_color=SUBTEXTO).pack(pady=(4,0))
                ctk.CTkLabel(card, text=valor, font=ctk.CTkFont(size=11, weight="bold"),
                            text_color=cor).pack(pady=(0,4))

        except Exception as e:
            ctk.CTkLabel(resultado_frame, text=f"❌ Erro: {str(e)}", 
                        font=ctk.CTkFont(size=11), text_color=VERMELHO).pack(padx=20, pady=10)

    def _limpar_calculadora(self, custos, pcts, resultado_frame):
        """Limpa os campos da calculadora"""
        for e in custos.values():
            e.delete(0, "end")
            e.insert(0, "0.00")
        for e in pcts.values():
            e.delete(0, "end")
            e.insert(0, "0")
        for w in resultado_frame.winfo_children():
            w.destroy()

# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()