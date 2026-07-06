import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, ROUND_HALF_UP
import math


VERMELHO = "#969696"
VERMELHO_ESCURO = "#8B0000"
FUNDO_DARK = "#1a0404"
FUNDO_CARD = "#2a0808"
FUNDO_CAMPO = "#3a1010"
BRANCO = "#FFFFFF"
CINZA_CLARO = "#ffcccc"
CINZA_MEDIO = "#ff9999"
VERDE = "#22c55e"
VERDE_CLARO = "#bbf7d0"
AMARELO = "#fbbf24"


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


class CampoMonetario(tk.Frame):
    def __init__(self, parent, label, **kwargs):
        super().__init__(parent, bg=FUNDO_CARD, **kwargs)
        self.var = tk.StringVar(value="0,00")

        tk.Label(
            self, text=label, bg=FUNDO_CARD, fg=CINZA_CLARO,
            font=("Segoe UI", 10), anchor="w", width=26
        ).pack(side="left", padx=(0, 8))

        frame_entry = tk.Frame(self, bg=FUNDO_CAMPO, highlightbackground=VERMELHO_ESCURO,
                               highlightthickness=1)
        frame_entry.pack(side="left")

        tk.Label(frame_entry, text="R$", bg=FUNDO_CAMPO, fg=CINZA_MEDIO,
                 font=("Segoe UI", 10)).pack(side="left", padx=(8, 4))

        self.entry = tk.Entry(
            frame_entry, textvariable=self.var, width=10,
            bg=FUNDO_CAMPO, fg=BRANCO, insertbackground=BRANCO,
            relief="flat", font=("Segoe UI", 11, "bold"),
            justify="right"
        )
        self.entry.pack(side="left", padx=(0, 8), pady=5)
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, event):
        val = self.var.get().replace(",", ".")
        try:
            float(val)
            if val in ("0.00", "0,00", "0"):
                self.var.set("")
        except ValueError:
            self.var.set("")

    def _on_focus_out(self, event):
        val = self.var.get().strip().replace(",", ".")
        try:
            num = float(val)
            self.var.set(f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        except ValueError:
            self.var.set("0,00")

    def get_value(self) -> float:
        val = self.var.get().replace(".", "").replace(",", ".")
        try:
            return float(val)
        except ValueError:
            return 0.0


class CampoPercentual(tk.Frame):
    def __init__(self, parent, label, **kwargs):
        super().__init__(parent, bg=FUNDO_CARD, **kwargs)
        self.var = tk.StringVar(value="0")

        tk.Label(
            self, text=label, bg=FUNDO_CARD, fg=CINZA_CLARO,
            font=("Segoe UI", 10), anchor="w", width=26
        ).pack(side="left", padx=(0, 8))

        frame_entry = tk.Frame(self, bg=FUNDO_CAMPO, highlightbackground=VERMELHO_ESCURO,
                               highlightthickness=1)
        frame_entry.pack(side="left")

        self.entry = tk.Entry(
            frame_entry, textvariable=self.var, width=8,
            bg=FUNDO_CAMPO, fg=BRANCO, insertbackground=BRANCO,
            relief="flat", font=("Segoe UI", 11, "bold"),
            justify="right"
        )
        self.entry.pack(side="left", padx=(8, 2), pady=5)
        self.entry.bind("<FocusIn>", lambda e: self.var.set("") if self.var.get() == "0" else None)
        self.entry.bind("<FocusOut>", self._on_focus_out)

        tk.Label(frame_entry, text="%", bg=FUNDO_CAMPO, fg=CINZA_MEDIO,
                 font=("Segoe UI", 10)).pack(side="left", padx=(0, 8))

    def _on_focus_out(self, event):
        val = self.var.get().strip().replace(",", ".")
        try:
            num = float(val)
            self.var.set(f"{num:.2f}".rstrip("0").rstrip(".") or "0")
        except ValueError:
            self.var.set("0")

    def get_value(self) -> float:
        val = self.var.get().replace(",", ".")
        try:
            return float(val)
        except ValueError:
            return 0.0


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Precificação — GAV")
        self.configure(bg=FUNDO_DARK)
        self.resizable(False, False)
        self._build_ui()
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")

    def _separador(self, parent):
        tk.Frame(parent, bg=VERMELHO_ESCURO, height=1).pack(fill="x", pady=8)

    def _titulo_secao(self, parent, texto):
        tk.Label(
            parent, text=texto, bg=FUNDO_CARD, fg=VERMELHO,
            font=("Segoe UI", 11, "bold"), anchor="w"
        ).pack(fill="x", pady=(12, 4))

    def _card(self, parent):
        frame = tk.Frame(parent, bg=FUNDO_CARD, padx=20, pady=12)
        frame.pack(fill="x", padx=20, pady=6)
        return frame

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=VERMELHO, pady=14)
        header.pack(fill="x")
        tk.Label(header, text="SISTEMA DE PRECIFICAÇÃO",
                 bg=VERMELHO, fg=BRANCO, font=("Segoe UI", 16, "bold")).pack()
        tk.Label(header, text="Calcule o preço de venda ideal sem prejuízo",
                 bg=VERMELHO, fg=CINZA_CLARO, font=("Segoe UI", 9)).pack()

        # Corpo principal com scroll
        canvas = tk.Canvas(self, bg=FUNDO_DARK, highlightthickness=0, width=580, height=600)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.frame_scroll = tk.Frame(canvas, bg=FUNDO_DARK)
        canvas.create_window((0, 0), window=self.frame_scroll, anchor="nw")
        self.frame_scroll.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # ---- SEÇÃO 1: CUSTOS DO PRODUTO ----
        card1 = self._card(self.frame_scroll)
        self._titulo_secao(card1, "📦  CUSTOS DO PRODUTO")

        self.f_preco_custo = CampoMonetario(card1, "Preço de custo da peça")
        self.f_preco_custo.pack(fill="x", pady=3)

        self.f_frete = CampoMonetario(card1, "Frete de compra")
        self.f_frete.pack(fill="x", pady=3)

        self._separador(card1)

        tk.Label(card1, text="🏷️  Etiquetas", bg=FUNDO_CARD, fg=CINZA_MEDIO,
                 font=("Segoe UI", 9, "italic")).pack(anchor="w")

        self.f_etiq_interna = CampoMonetario(card1, "Etiqueta interna")
        self.f_etiq_interna.pack(fill="x", pady=3)

        self.f_etiq_externa = CampoMonetario(card1, "Etiqueta externa")
        self.f_etiq_externa.pack(fill="x", pady=3)

        self.f_etiq_termo = CampoMonetario(card1, "Etiqueta termocolante")
        self.f_etiq_termo.pack(fill="x", pady=3)

        self._separador(card1)

        tk.Label(card1, text="🛍️  Embalagem", bg=FUNDO_CARD, fg=CINZA_MEDIO,
                 font=("Segoe UI", 9, "italic")).pack(anchor="w")

        self.f_embalagem = CampoMonetario(card1, "Embalagem")
        self.f_embalagem.pack(fill="x", pady=3)

        self.f_sacola = CampoMonetario(card1, "Sacola")
        self.f_sacola.pack(fill="x", pady=3)

        self._separador(card1)

        self.f_outros = CampoMonetario(card1, "Outros custos")
        self.f_outros.pack(fill="x", pady=3)

        # ---- SEÇÃO 2: PERCENTUAIS ----
        card2 = self._card(self.frame_scroll)
        self._titulo_secao(card2, "📊  PERCENTUAIS")

        self.f_impostos = CampoPercentual(card2, "Impostos (%)")
        self.f_impostos.pack(fill="x", pady=3)

        self.f_cartao = CampoPercentual(card2, "Taxa de cartão (%)")
        self.f_cartao.pack(fill="x", pady=3)

        self.f_comissao = CampoPercentual(card2, "Comissão de vendedor (%)")
        self.f_comissao.pack(fill="x", pady=3)

        # ---- SEÇÃO 3: MARGEM ----
        card3 = self._card(self.frame_scroll)
        self._titulo_secao(card3, "💰  MARGEM DE LUCRO")

        self.f_lucro = CampoPercentual(card3, "Percentual de lucro desejado (%)")
        self.f_lucro.pack(fill="x", pady=3)

        # Aviso de margem mínima
        self.label_aviso = tk.Label(card3, text="", bg=FUNDO_CARD,
                                    font=("Segoe UI", 9), anchor="w")
        self.label_aviso.pack(fill="x", pady=(4, 0))

        # ---- BOTÃO CALCULAR ----
        btn_frame = tk.Frame(self.frame_scroll, bg=FUNDO_DARK, pady=10)
        btn_frame.pack(fill="x", padx=20)

        self.btn_calcular = tk.Button(
            btn_frame, text="▶  CALCULAR PREÇO DE VENDA",
            command=self.calcular,
            bg=VERMELHO, fg=BRANCO, activebackground=VERMELHO_ESCURO,
            activeforeground=BRANCO, relief="flat",
            font=("Segoe UI", 12, "bold"), pady=12, cursor="hand2"
        )
        self.btn_calcular.pack(fill="x")

        btn_limpar = tk.Button(
            btn_frame, text="↺  Limpar Campos",
            command=self.limpar,
            bg=FUNDO_CARD, fg=CINZA_MEDIO, activebackground=FUNDO_CAMPO,
            activeforeground=BRANCO, relief="flat",
            font=("Segoe UI", 9), pady=6, cursor="hand2"
        )
        btn_limpar.pack(fill="x", pady=(6, 0))

        # ---- RESULTADO ----
        self.frame_resultado = tk.Frame(self.frame_scroll, bg=FUNDO_DARK)
        self.frame_resultado.pack(fill="x", padx=20, pady=(0, 20))

    def calcular(self):
        try:
            preco_custo = self.f_preco_custo.get_value()
            frete = self.f_frete.get_value()
            etiq_int = self.f_etiq_interna.get_value()
            etiq_ext = self.f_etiq_externa.get_value()
            etiq_termo = self.f_etiq_termo.get_value()
            embalagem = self.f_embalagem.get_value()
            sacola = self.f_sacola.get_value()
            outros = self.f_outros.get_value()

            pct_impostos = self.f_impostos.get_value()
            pct_cartao = self.f_cartao.get_value()
            pct_comissao = self.f_comissao.get_value()
            pct_lucro = self.f_lucro.get_value()

            # Custo total
            custo_total = (preco_custo + frete + etiq_int + etiq_ext +
                           etiq_termo + embalagem + sacola + outros)

            # Total percentual
            total_pct = (pct_impostos + pct_cartao + pct_comissao + pct_lucro) / 100

            if total_pct >= 1.0:
                messagebox.showerror(
                    "Erro de Cálculo",
                    "A soma dos percentuais é maior ou igual a 100%!\n"
                    "Isso tornaria o preço de venda infinito.\n"
                    "Por favor, revise os percentuais."
                )
                return

            if custo_total <= 0:
                messagebox.showwarning("Atenção", "Informe ao menos o preço de custo do produto.")
                return

            # Preço de venda
            preco_venda = custo_total / (1 - total_pct)
            preco_arredondado = arredondar_preco(preco_venda)

            # Lucro em R$
            lucro_rs = preco_arredondado - custo_total
            lucro_pct_real = (lucro_rs / preco_arredondado * 100) if preco_arredondado > 0 else 0
            markup = (preco_arredondado / custo_total) if custo_total > 0 else 0

            self._mostrar_resultado(
                custo_total, preco_venda, preco_arredondado,
                lucro_rs, lucro_pct_real, markup,
                pct_impostos, pct_cartao, pct_comissao, pct_lucro, total_pct * 100,
                preco_custo, frete, etiq_int, etiq_ext, etiq_termo, embalagem, sacola, outros
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro no cálculo:\n{e}")

    def _mostrar_resultado(self, custo_total, preco_venda, preco_arrend,
                           lucro_rs, lucro_pct, markup,
                           imp, cart, com, luc, total_pct,
                           pc, fr, ei, ee, et, em, sa, ou):

        # Limpa resultado anterior
        for w in self.frame_resultado.winfo_children():
            w.destroy()

        card = tk.Frame(self.frame_resultado, bg=FUNDO_CARD, padx=20, pady=16)
        card.pack(fill="x")

        tk.Label(card, text="RESULTADO DO CÁLCULO", bg=FUNDO_CARD, fg=VERMELHO,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))

        # --- Detalhamento dos custos ---
        tk.Label(card, text="Detalhamento dos custos:", bg=FUNDO_CARD, fg=CINZA_MEDIO,
                 font=("Segoe UI", 9, "italic")).pack(anchor="w")

        itens = [
            ("Preço de custo", pc),
            ("Frete de compra", fr),
            ("Etiqueta interna", ei),
            ("Etiqueta externa", ee),
            ("Etiqueta termocolante", et),
            ("Embalagem", em),
            ("Sacola", sa),
            ("Outros custos", ou),
        ]

        for nome, valor in itens:
            if valor > 0:
                linha = tk.Frame(card, bg=FUNDO_CARD)
                linha.pack(fill="x", pady=1)
                tk.Label(linha, text=f"  • {nome}", bg=FUNDO_CARD, fg=CINZA_CLARO,
                         font=("Segoe UI", 9), anchor="w").pack(side="left")
                tk.Label(linha, text=f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                         bg=FUNDO_CARD, fg=BRANCO, font=("Segoe UI", 9, "bold")).pack(side="right")

        tk.Frame(card, bg=VERMELHO_ESCURO, height=1).pack(fill="x", pady=6)

        # Custo total
        linha_ct = tk.Frame(card, bg=FUNDO_CAMPO, padx=10, pady=6)
        linha_ct.pack(fill="x", pady=2)
        tk.Label(linha_ct, text="CUSTO TOTAL", bg=FUNDO_CAMPO, fg=CINZA_MEDIO,
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Label(linha_ct, text=f"R$ {custo_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                 bg=FUNDO_CAMPO, fg=BRANCO, font=("Segoe UI", 11, "bold")).pack(side="right")

        # Percentuais
        tk.Label(card, text="\nPercentuais aplicados:", bg=FUNDO_CARD, fg=CINZA_MEDIO,
                 font=("Segoe UI", 9, "italic")).pack(anchor="w")

        pcts = [
            (f"Impostos", imp),
            (f"Taxa de cartão", cart),
            (f"Comissão vendedor", com),
            (f"Margem de lucro", luc),
        ]
        for nome, val in pcts:
            if val > 0:
                linha = tk.Frame(card, bg=FUNDO_CARD)
                linha.pack(fill="x", pady=1)
                tk.Label(linha, text=f"  • {nome}", bg=FUNDO_CARD, fg=CINZA_CLARO,
                         font=("Segoe UI", 9), anchor="w").pack(side="left")
                tk.Label(linha, text=f"{val:.2f}%".replace(".", ","),
                         bg=FUNDO_CARD, fg=CINZA_MEDIO, font=("Segoe UI", 9)).pack(side="right")

        linha = tk.Frame(card, bg=FUNDO_CARD)
        linha.pack(fill="x", pady=1)
        tk.Label(linha, text="  TOTAL PERCENTUAL", bg=FUNDO_CARD, fg=CINZA_MEDIO,
                 font=("Segoe UI", 9, "bold")).pack(side="left")
        tk.Label(linha, text=f"{total_pct:.2f}%".replace(".", ","),
                 bg=FUNDO_CARD, fg=AMARELO, font=("Segoe UI", 9, "bold")).pack(side="right")

        tk.Frame(card, bg=VERMELHO, height=2).pack(fill="x", pady=10)

        # Preço de venda calculado
        linha_pv = tk.Frame(card, bg=FUNDO_CARD)
        linha_pv.pack(fill="x", pady=2)
        tk.Label(linha_pv, text="Preço calculado:", bg=FUNDO_CARD, fg=CINZA_CLARO,
                 font=("Segoe UI", 10)).pack(side="left")
        tk.Label(linha_pv, text=f"R$ {preco_venda:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                 bg=FUNDO_CARD, fg=CINZA_MEDIO, font=("Segoe UI", 10)).pack(side="right")

        # Preço sugerido (arredondado)
        frame_destaque = tk.Frame(card, bg=VERMELHO, padx=12, pady=12)
        frame_destaque.pack(fill="x", pady=6)
        tk.Label(frame_destaque, text="💰  PREÇO SUGERIDO DE VENDA",
                 bg=VERMELHO, fg=CINZA_CLARO, font=("Segoe UI", 10, "bold")).pack()
        tk.Label(frame_destaque,
                 text=f"R$ {preco_arrend:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                 bg=VERMELHO, fg=BRANCO, font=("Segoe UI", 22, "bold")).pack()

        # Indicadores de lucro
        frame_indicadores = tk.Frame(card, bg=FUNDO_CARD)
        frame_indicadores.pack(fill="x", pady=8)

        cor_lucro = VERDE if lucro_rs > 0 else "#ef4444"
        cor_bg_lucro = "#052e16" if lucro_rs > 0 else "#450a0a"

        def indicador(parent, titulo, valor, cor, cor_bg):
            f = tk.Frame(parent, bg=cor_bg, padx=10, pady=8)
            f.pack(side="left", fill="both", expand=True, padx=3)
            tk.Label(f, text=titulo, bg=cor_bg, fg=cor,
                     font=("Segoe UI", 8)).pack()
            tk.Label(f, text=valor, bg=cor_bg, fg=cor,
                     font=("Segoe UI", 11, "bold")).pack()

        indicador(frame_indicadores, "Lucro R$",
                  f"R$ {lucro_rs:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                  VERDE_CLARO if lucro_rs > 0 else "#fca5a5", cor_bg_lucro)

        indicador(frame_indicadores, "Lucro %",
                  f"{lucro_pct:.1f}%".replace(".", ","),
                  VERDE_CLARO if lucro_rs > 0 else "#fca5a5", cor_bg_lucro)

        indicador(frame_indicadores, "Markup",
                  f"{markup:.2f}x".replace(".", ","),
                  VERDE_CLARO if markup >= 1 else "#fca5a5",
                  "#052e16" if markup >= 1 else "#450a0a")

        # Fórmula exibida
        tk.Frame(card, bg=VERMELHO_ESCURO, height=1).pack(fill="x", pady=8)
        tk.Label(card, text="Fórmula aplicada:", bg=FUNDO_CARD, fg=CINZA_MEDIO,
                 font=("Segoe UI", 8, "italic")).pack(anchor="w")

        divisor = 1 - (total_pct / 100)
        formula_texto = (
            f"R$ {custo_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") +
            f" ÷ (1 - {total_pct:.2f}%".replace(".", ",") + ")" +
            f" = R$ {preco_venda:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        tk.Label(card, text=formula_texto, bg=FUNDO_CARD, fg=CINZA_CLARO,
                 font=("Courier New", 9)).pack(anchor="w")

    def limpar(self):
        campos = [
            self.f_preco_custo, self.f_frete, self.f_etiq_interna,
            self.f_etiq_externa, self.f_etiq_termo, self.f_embalagem,
            self.f_sacola, self.f_outros
        ]
        for c in campos:
            c.var.set("0,00")

        pcts = [self.f_impostos, self.f_cartao, self.f_comissao, self.f_lucro]
        for p in pcts:
            p.var.set("0")

        for w in self.frame_resultado.winfo_children():
            w.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()