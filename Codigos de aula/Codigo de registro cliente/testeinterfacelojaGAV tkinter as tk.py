import tkinter as tk
from tkinter import ttk, messagebox, font
import mysql.connector
from mysql.connector import Error

# ── Paleta de cores ──────────────────────────────────────────────────────────
BG        = "#F8F7F4"
SIDEBAR   = "#FFFFFF"
CARD      = "#FFFFFF"
BORDER    = "#E4E3DC"
ACCENT    = "#534AB7"
ACCENT_LT = "#EEEDFE"
ACCENT_TX = "#3C3489"
TEXT_PRI  = "#1A1A18"
TEXT_SEC  = "#888780"
TEXT_HINT = "#B4B2A9"
SUCCESS   = "#0F6E56"
SUCCESS_B = "#E1F5EE"
DANGER    = "#A32D2D"
DANGER_B  = "#FCEBEB"
WARNING_B = "#FAEEDA"
WARNING_T = "#633806"

TIPO_COLORS = {
    "Camiseta": ("#EEEDFE", "#3C3489"),
    "Calça":    ("#E1F5EE", "#085041"),
    "Calção":   ("#FAEEDA", "#633806"),
    "Regata":   ("#FAECE7", "#712B13"),
}

# ── Conexão MySQL ─────────────────────────────────────────────────────────────
db = None
mycursor = None

def conectar():
    global db, mycursor
    try:
        db = mysql.connector.connect(
            host="localhost", user="root", password="root", database="teste"
        )
        mycursor = db.cursor(buffered=True)
        return True
    except Error as e:
        messagebox.showerror("Erro de conexão", f"Não foi possível conectar ao MySQL:\n{e}")
        return False

# ── Helpers UI ────────────────────────────────────────────────────────────────
def frame(parent, bg=BG, **kw):
    return tk.Frame(parent, bg=bg, **kw)

def label(parent, text, size=13, weight="normal", color=TEXT_PRI, bg=BG, **kw):
    return tk.Label(parent, text=text, font=("Helvetica", size, weight),
                    fg=color, bg=bg, **kw)

def sep(parent, bg=BORDER):
    return tk.Frame(parent, bg=bg, height=1)

# ── Aplicação principal ───────────────────────────────────────────────────────
class EstoqueApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Estoque")
        self.geometry("1000x660")
        self.minsize(860, 560)
        self.configure(bg=BG)
        self.resizable(True, True)
        
    def __inti__(self):
        super().__init__()
        
        icone = tk.PhotoImage(file="icone.png")
        self.iconphoto(True, icone)
        
        self.title("Sistema de Estoque")

        # Estilo ttk
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview",
                        background=CARD, fieldbackground=CARD,
                        foreground=TEXT_PRI, font=("Helvetica", 12),
                        rowheight=40, borderwidth=0)
        style.configure("Treeview.Heading",
                        background=BG, foreground=TEXT_SEC,
                        font=("Helvetica", 11, "normal"), relief="flat",
                        borderwidth=0, padding=(8, 6))
        style.map("Treeview",
                  background=[("selected", ACCENT_LT)],
                  foreground=[("selected", ACCENT_TX)])
        style.configure("Vertical.TScrollbar", background=BG,
                        troughcolor=BG, borderwidth=0, arrowsize=12)
        style.configure("TSeparator", background=BORDER)

        self.current_view = None
        self._build_layout()
        self.show_lista()

    # ── Layout base ──────────────────────────────────────────────────────────
    def _build_layout(self):
        self.sidebar = frame(self, bg=SIDEBAR, width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        sep(self.sidebar, bg=BORDER).pack(side="right", fill="y")

        self._build_sidebar()

        self.content = frame(self, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)
        


    def _build_sidebar(self):
        top = frame(self.sidebar, bg=SIDEBAR)
        top.pack(fill="x", padx=16, pady=(20, 16))

        ico = frame(top, bg=ACCENT_LT, width=32, height=32)
        ico.pack(side="left")
        ico.pack_propagate(False)
        label(ico, "📦", size=16, bg=ACCENT_LT).place(relx=.5, rely=.5, anchor="center") 

        info = frame(top, bg=SIDEBAR)
        info.pack(side="left", padx=(8, 0))
        label(info, "Estoque", size=13, weight="bold", bg=SIDEBAR).pack(anchor="w")
        label(info, "Sistema v2.0", size=10, color=TEXT_SEC, bg=SIDEBAR).pack(anchor="w")

        sep(self.sidebar).pack(fill="x")

        nav = frame(self.sidebar, bg=SIDEBAR)
        nav.pack(fill="x", padx=10, pady=10)

        self.nav_btns = {}
        for key, icon, text in [("lista", "☰", "  Itens"), ("cadastro", "+", "  Cadastrar")]:
            btn = tk.Button(nav, text=f" {icon}  {text}", font=("Helvetica", 12),
                            fg=TEXT_SEC, bg=SIDEBAR, activebackground=ACCENT_LT,
                            activeforeground=ACCENT_TX, relief="flat", anchor="w",
                            padx=8, pady=7, cursor="hand2",
                            command=lambda k=key: self._nav(k))
            btn.pack(fill="x", pady=2)
            self.nav_btns[key] = btn

        sep(self.sidebar).pack(fill="x", pady=(4, 0))

        self.stats_frame = frame(self.sidebar, bg=SIDEBAR)
        self.stats_frame.pack(fill="x", padx=14, pady=14)
        label(self.stats_frame, "RESUMO", size=9, color=TEXT_HINT,
              bg=SIDEBAR).pack(anchor="w", pady=(0, 8))

        self.lbl_skus   = self._stat_row("SKUs", "0")
        self.lbl_units  = self._stat_row("Unidades", "0")
        self.lbl_valor  = self._stat_row("Valor em estoque", "R$ 0,00")

    def _stat_row(self, label_text, default):
        f = frame(self.sidebar, bg=SIDEBAR)
        f.pack(fill="x", padx=14, pady=3)
        label(f, label_text, size=10, color=TEXT_SEC, bg=SIDEBAR).pack(anchor="w")
        v = tk.StringVar(value=default)
        tk.Label(f, textvariable=v, font=("Helvetica", 14, "bold"),
                 fg=TEXT_PRI, bg=SIDEBAR).pack(anchor="w")
        return v

    def _nav(self, key):
        for k, btn in self.nav_btns.items():
            if k == key:
                btn.configure(bg=ACCENT_LT, fg=ACCENT_TX, font=("Helvetica", 12, "bold"))
            else:
                btn.configure(bg=SIDEBAR, fg=TEXT_SEC, font=("Helvetica", 12))
        if key == "lista":
            self.show_lista()
        else:
            self.show_cadastro()

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ── Stats ─────────────────────────────────────────────────────────────────
    def _update_stats(self, rows):
        total_un = sum(r[6] for r in rows)
        total_val = sum(r[9] * r[6] for r in rows)
        self.lbl_skus.set(str(len(rows)))
        self.lbl_units.set(f"{total_un:,}".replace(",", "."))
        self.lbl_valor.set(f"R$ {total_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # ── Vista: Lista ──────────────────────────────────────────────────────────
    def show_lista(self):
        self._nav_active("lista")
        self._clear_content()

        outer = frame(self.content, bg=BG)
        outer.pack(fill="both", expand=True, padx=28, pady=24)

        # Cabeçalho
        hdr = frame(outer, bg=BG)
        hdr.pack(fill="x", pady=(0, 16))

        label(hdr, "Itens em estoque", size=18, weight="bold").pack(side="left")

        btn_add = tk.Button(hdr, text="  + Cadastrar", font=("Helvetica", 12),
                            fg=CARD, bg=ACCENT, activebackground=ACCENT_TX,
                            activeforeground=CARD, relief="flat", padx=14, pady=7,
                            cursor="hand2", command=lambda: self._nav("cadastro"))
        btn_add.pack(side="right")

        # Barra de busca
        search_frame = frame(outer, bg=CARD, highlightbackground=BORDER,
                             highlightthickness=1)
        search_frame.pack(fill="x", pady=(0, 12))

        label(search_frame, "🔍", size=13, bg=CARD).pack(side="left", padx=(10, 4))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self._filtrar())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                font=("Helvetica", 12), fg=TEXT_PRI, bg=CARD,
                                relief="flat", insertbackground=ACCENT)
        search_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
        search_entry.insert(0, "")

        # Filtros de tipo
        filter_row = frame(outer, bg=BG)
        filter_row.pack(fill="x", pady=(0, 14))

        self.filter_var = tk.StringVar(value="Todos")
        for f_text in ["Todos", "Camiseta", "Calça", "Calção", "Regata"]:
            btn = tk.Button(filter_row, text=f_text, font=("Helvetica", 11),
                            relief="flat", padx=10, pady=5, cursor="hand2",
                            command=lambda t=f_text: self._set_filter(t))
            btn.pack(side="left", padx=(0, 6))
            btn.config(bg=ACCENT_LT if f_text == "Todos" else BG,
                       fg=ACCENT_TX if f_text == "Todos" else TEXT_SEC)
            setattr(self, f"fbtn_{f_text}", btn)

        # Tabela
        cols = ("nome", "tipo", "tamanho", "marca", "qtd", "compra", "venda")
        tree_frame = frame(outer, bg=CARD, highlightbackground=BORDER,
                           highlightthickness=1)
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings",
                                 selectmode="browse")

        headers = [("nome", "Nome", 220), ("tipo", "Tipo", 90),
                   ("tamanho", "Tam.", 55), ("marca", "Marca", 110),
                   ("qtd", "Qtd.", 60), ("compra", "Compra", 90), ("venda", "Venda", 90)]
        for col, text, w in headers:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, minwidth=40, anchor="w")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.tag_configure("odd",  background="#FAFAF8")
        self.tree.tag_configure("even", background=CARD)
        self.tree.bind("<ButtonRelease-1>", self._on_tree_click)

        self._carregar_itens()

    def _nav_active(self, key):
        for k, btn in self.nav_btns.items():
            if k == key:
                btn.configure(bg=ACCENT_LT, fg=ACCENT_TX, font=("Helvetica", 12, "bold"))
            else:
                btn.configure(bg=SIDEBAR, fg=TEXT_SEC, font=("Helvetica", 12))

    def _carregar_itens(self):
        self.tree.delete(*self.tree.get_children())
        try:
            mycursor.execute("SELECT * FROM itens")
            self.all_rows = mycursor.fetchall()
        except Error as e:
            messagebox.showerror("Erro", str(e))
            self.all_rows = []
        self._update_stats(self.all_rows)
        self._filtrar()

    def _set_filter(self, tipo):
        self.filter_var.set(tipo)
        for f_text in ["Todos", "Camiseta", "Calça", "Calção", "Regata"]:
            btn = getattr(self, f"fbtn_{f_text}", None)
            if btn:
                active = f_text == tipo
                btn.config(bg=ACCENT_LT if active else BG,
                           fg=ACCENT_TX if active else TEXT_SEC,
                           font=("Helvetica", 11, "bold" if active else "normal"))
        self._filtrar()

    def _filtrar(self):
        q = self.search_var.get().lower() if hasattr(self, "search_var") else ""
        f = self.filter_var.get() if hasattr(self, "filter_var") else "Todos"
        self.tree.delete(*self.tree.get_children())
        filtrados = []
        for row in self.all_rows:
            match_q = q in row[1].lower() or q in row[5].lower() or q in row[2].lower()
            match_f = f == "Todos" or row[2] == f
            if match_q and match_f:
                filtrados.append(row)
        for i, row in enumerate(filtrados):
            tag = "odd" if i % 2 else "even"
            venda = f"R$ {row[9]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            compra = f"R$ {row[8]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            self.tree.insert("", "end", iid=str(row[0]),
                             values=(row[1], row[2], row[4], row[5], row[6], compra, venda),
                             tags=(tag,))

    def _on_tree_click(self, event):
        sel = self.tree.selection()
        if sel:
            item_id = int(sel[0])
            row = next((r for r in self.all_rows if r[0] == item_id), None)
            if row:
                self.show_detalhe(row)

    # ── Vista: Detalhe ────────────────────────────────────────────────────────
    def show_detalhe(self, row):
        win = tk.Toplevel(self)
        win.title(f"Detalhe — {row[1]}")
        win.geometry("520x480")
        win.configure(bg=BG)
        win.resizable(False, False)
        win.grab_set()

        outer = frame(win, bg=BG)
        outer.pack(fill="both", expand=True, padx=24, pady=20)

        tipo_bg, tipo_fg = TIPO_COLORS.get(row[2], (ACCENT_LT, ACCENT_TX))
        badge = tk.Label(outer, text=f" {row[2]} ", font=("Helvetica", 10),
                         fg=tipo_fg, bg=tipo_bg, padx=6, pady=2)
        badge.pack(anchor="w", pady=(0, 6))

        label(outer, row[1], size=17, weight="bold").pack(anchor="w")
        label(outer, f"ID #{row[0]}  ·  {row[5]}", size=11, color=TEXT_SEC).pack(anchor="w", pady=(2, 14))

        grid_f = frame(outer, bg=BG)
        grid_f.pack(fill="x", pady=(0, 14))
        infos = [("Quantidade", f"{row[6]} unidades"), ("Tamanho", row[4]),
                 ("Modelo", row[3]), ("Fornecedor", row[7])]
        for i, (lbl, val) in enumerate(infos):
            c = frame(grid_f, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
            c.grid(row=i//2, column=i%2, padx=(0 if i%2 else 0, 8 if i%2==0 else 0),
                   pady=4, sticky="ew")
            grid_f.columnconfigure(i%2, weight=1)
            label(c, lbl, size=10, color=TEXT_SEC, bg=CARD).pack(anchor="w", padx=12, pady=(8, 0))
            label(c, val, size=13, weight="bold", bg=CARD).pack(anchor="w", padx=12, pady=(0, 8))

        price_row = frame(outer, bg=BG)
        price_row.pack(fill="x", pady=(0, 10))
        for bg_c, fg_c, lbl_t, val in [(SUCCESS_B, SUCCESS, "Preço de compra", f"R$ {row[8]:,.2f}"),
                                        (ACCENT_LT, ACCENT_TX, "Preço de venda", f"R$ {row[9]:,.2f}")]:
            p = frame(price_row, bg=bg_c, highlightbackground=BORDER, highlightthickness=1)
            p.pack(side="left", fill="x", expand=True, padx=(0, 6))
            label(p, lbl_t, size=10, color=fg_c, bg=bg_c).pack(anchor="w", padx=12, pady=(8, 0))
            label(p, val.replace(",", "X").replace(".", ",").replace("X", "."),
                  size=17, weight="bold", color=fg_c, bg=bg_c).pack(anchor="w", padx=12, pady=(0, 8))

        if row[8] > 0:
            margem = ((row[9] - row[8]) / row[8]) * 100
            lucro = row[9] - row[8]
            m_frame = frame(outer, bg=BG, highlightbackground=BORDER, highlightthickness=1)
            m_frame.pack(fill="x", pady=(0, 14))
            label(m_frame, "Margem de lucro", size=10, color=TEXT_SEC).pack(anchor="w", padx=12, pady=(8, 2))
            label(m_frame, f"{margem:.1f}%  ·  R$ {lucro:.2f} por unidade",
                  size=13, weight="bold").pack(anchor="w", padx=12, pady=(0, 8))

        btns = frame(outer, bg=BG)
        btns.pack(fill="x", pady=(4, 0))
        tk.Button(btns, text="  🗑  Remover item", font=("Helvetica", 12),
                  fg=DANGER, bg=DANGER_B, activebackground="#F7C1C1",
                  relief="flat", padx=14, pady=7, cursor="hand2",
                  command=lambda: self._deletar(row[0], row[1], win)).pack(side="left")
        tk.Button(btns, text="Fechar", font=("Helvetica", 12),
                  fg=TEXT_SEC, bg=BG, relief="flat", padx=14, pady=7, cursor="hand2",
                  command=win.destroy).pack(side="right")

    def _deletar(self, item_id, nome, win):
        if not messagebox.askyesno("Confirmar", f'Remover "{nome}"?', parent=win):
            return
        try:
            mycursor.execute("DELETE FROM itens WHERE id = %s", (item_id,))
            db.commit()
            win.destroy()
            self._toast(f'"{nome}" removido com sucesso.')
            self._carregar_itens()
        except Error as e:
            messagebox.showerror("Erro", str(e))

    # ── Vista: Cadastro ───────────────────────────────────────────────────────
    def show_cadastro(self):
        self._nav_active("cadastro")
        self._clear_content()

        outer = frame(self.content, bg=BG)
        outer.pack(fill="both", expand=True, padx=28, pady=24)

        label(outer, "Cadastrar item", size=18, weight="bold").pack(anchor="w")
        label(outer, "Preencha os dados do novo produto", size=12,
              color=TEXT_SEC).pack(anchor="w", pady=(2, 20))

        form = frame(outer, bg=BG)
        form.pack(fill="both", expand=True)
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        self.fvars = {}
        self.ferrs = {}

        def field(parent, name, label_text, row, col, colspan=1, etype="entry",
                  options=None, width=None):
            f = frame(parent, bg=BG)
            f.grid(row=row, column=col, columnspan=colspan,
                   sticky="ew", padx=(0, 12 if col == 0 else 0), pady=5)
            tk.Label(f, text=label_text, font=("Helvetica", 10, "bold"),
                     fg=TEXT_SEC, bg=BG).pack(anchor="w")
            var = tk.StringVar()
            self.fvars[name] = var
            if etype == "entry":
                e = tk.Entry(f, textvariable=var, font=("Helvetica", 12),
                             fg=TEXT_PRI, bg=CARD, relief="flat", insertbackground=ACCENT,
                             highlightthickness=1, highlightbackground=BORDER,
                             highlightcolor=ACCENT)
                e.pack(fill="x", ipady=7)
            elif etype == "combo":
                e = ttk.Combobox(f, textvariable=var, values=options,
                                 font=("Helvetica", 12), state="readonly")
                e.current(0)
                e.pack(fill="x", ipady=4)
            err = tk.Label(f, text="", font=("Helvetica", 10), fg=DANGER, bg=BG)
            err.pack(anchor="w")
            self.ferrs[name] = err
            return var

        field(form, "nome", "Nome do item", 0, 0, colspan=2)

        tipo_var = field(form, "tipo", "Tipo", 1, 0,
                         etype="combo", options=["Camiseta", "Calça", "Calção", "Regata"])
        field(form, "tamanho", "Tamanho", 1, 1,
              etype="combo", options=["P", "M", "G", "GG"])

        self.modelo_frame_row = frame(form, bg=BG)
        self.modelo_frame_row.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.modelo_frame_row.columnconfigure(0, weight=1)
        self.modelo_frame_row.columnconfigure(1, weight=1)

        def build_modelo_fields(has_model):
            for w in self.modelo_frame_row.winfo_children():
                w.destroy()
            self.fvars.pop("modelo", None)
            self.ferrs.pop("modelo", None)
            if has_model:
                field(self.modelo_frame_row, "modelo", "Modelo", 0, 0,
                      etype="combo", options=["Manga Curta", "Manga Longa"])
                field(self.modelo_frame_row, "marca", "Marca", 0, 1)
            else:
                field(self.modelo_frame_row, "marca", "Marca", 0, 0, colspan=2)

        build_modelo_fields(True)

        def on_tipo_change(*_):
            t = tipo_var.get()
            build_modelo_fields(t in ("Camiseta", "Regata"))
            update_margem()

        tipo_var.trace("w", on_tipo_change)

        field(form, "quantidade", "Quantidade", 3, 0)
        field(form, "fornecedor", "Fornecedor",  3, 1)

        pc_var = field(form, "preco_compra", "Preço de compra (R$)", 4, 0)
        pv_var = field(form, "preco_venda",  "Preço de venda (R$)",  4, 1)

        # Preview de margem
        self.margem_lbl = tk.Label(form, text="", font=("Helvetica", 11),
                                   fg=SUCCESS, bg=SUCCESS_B, pady=6, padx=10)

        def update_margem(*_):
            try:
                pc = float(pc_var.get())
                pv = float(pv_var.get())
                if pc > 0 and pv > pc:
                    m = ((pv - pc) / pc) * 100
                    self.margem_lbl.config(
                        text=f"  Margem: {m:.1f}%  ·  Lucro de R$ {pv-pc:.2f} por unidade  ")
                    self.margem_lbl.grid(row=5, column=0, columnspan=2, sticky="ew", pady=6)
                else:
                    self.margem_lbl.grid_remove()
            except ValueError:
                self.margem_lbl.grid_remove()

        pc_var.trace("w", update_margem)
        pv_var.trace("w", update_margem)

        # Botões
        btn_row = frame(form, bg=BG)
        btn_row.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(14, 0))

        tk.Button(btn_row, text="  ✓  Cadastrar item", font=("Helvetica", 13, "bold"),
                  fg=CARD, bg=ACCENT, activebackground=ACCENT_TX, activeforeground=CARD,
                  relief="flat", padx=18, pady=9, cursor="hand2",
                  command=self._salvar).pack(side="left")
        tk.Button(btn_row, text="Cancelar", font=("Helvetica", 12),
                  fg=TEXT_SEC, bg=BG, relief="flat", padx=14, pady=9, cursor="hand2",
                  command=lambda: self._nav("lista")).pack(side="left", padx=(10, 0))

    def _salvar(self):
        v = self.fvars
        tipo = v["tipo"].get()
        tem_modelo = tipo in ("Camiseta", "Regata")
        nome     = v["nome"].get().strip()
        marca    = v["marca"].get().strip()
        qtd_str  = v["quantidade"].get().strip()
        forn     = v["fornecedor"].get().strip()
        pc_str   = v["preco_compra"].get().strip()
        pv_str   = v["preco_venda"].get().strip()
        modelo   = v.get("modelo", tk.StringVar()).get() if tem_modelo else "N/A"
        tamanho  = v["tamanho"].get()

        ok = True
        def err(k, msg):
            nonlocal ok
            if k in self.ferrs:
                self.ferrs[k].config(text=msg)
            if msg:
                ok = False

        for k in self.ferrs:
            self.ferrs[k].config(text="")

        err("nome", "" if nome else "Campo obrigatório")
        err("marca", "" if marca else "Campo obrigatório")
        err("fornecedor", "" if forn else "Campo obrigatório")

        try:
            qtd = int(qtd_str)
            if qtd < 0: raise ValueError
            err("quantidade", "")
        except ValueError:
            err("quantidade", "Número inteiro ≥ 0")

        try:
            pc = float(pc_str)
            if pc < 0: raise ValueError
            err("preco_compra", "")
        except ValueError:
            err("preco_compra", "Número válido ≥ 0")
            pc = None

        try:
            pv = float(pv_str)
            if pc is not None and pv < pc:
                err("preco_venda", "Deve ser ≥ preço de compra")
            else:
                err("preco_venda", "")
        except ValueError:
            err("preco_venda", "Número válido")
            pv = None

        if not ok:
            return

        try:
            sql = """INSERT INTO itens (nome, tipo, modelo, tamanho, marca,
                     quantidade, fornecedor, preco_compra, preco_venda)
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            mycursor.execute(sql, (nome, tipo, modelo, tamanho, marca,
                                   qtd, forn, pc, pv))
            db.commit()
            self._toast(f'"{nome}" cadastrado com sucesso!')
            self._nav("lista")
        except Error as e:
            messagebox.showerror("Erro ao salvar", str(e))

    # ── Toast ─────────────────────────────────────────────────────────────────
    def _toast(self, msg, tipo="success"):
        bg = SUCCESS_B if tipo == "success" else DANGER_B
        fg = SUCCESS   if tipo == "success" else DANGER
        t = tk.Toplevel(self)
        t.overrideredirect(True)
        t.attributes("-topmost", True)
        x = self.winfo_x() + self.winfo_width() - 340
        y = self.winfo_y() + 20
        t.geometry(f"+{x}+{y}")
        tk.Label(t, text=f"  {msg}  ", font=("Helvetica", 11),
                 fg=fg, bg=bg, pady=10, padx=6).pack()
        t.after(2800, t.destroy)


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if conectar():
        app = EstoqueApp()
        app.mainloop()
        if db and db.is_connected():
            db.close()