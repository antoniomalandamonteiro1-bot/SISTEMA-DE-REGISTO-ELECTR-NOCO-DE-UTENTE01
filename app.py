import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

FICHEIRO_DADOS = "sreu_dados.json"


class SREUGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SREU - Sistema de Registo Eletrónico de Utentes")
        self.root.geometry("800x550")
        self.root.configure(bg="#f4f6f9")

        self.utentes = self.carregar_dados()
        self.criar_componentes()

    def carregar_dados(self):
        if os.path.exists(FICHEIRO_DADOS):
            try:
                with open(FICHEIRO_DADOS, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def guardar_dados(self):
        with open(FICHEIRO_DADOS, "w", encoding="utf-8") as f:
            json.dump(self.utentes, f, ensure_ascii=False, indent=4)

    def criar_componentes(self):
        # Cabeçalho
        header = tk.Frame(self.root, bg="#0d6efd", pady=15)
        header.pack(fill="x")
        tk.Label(header, text="🏥 SREU - Sistema de Registo Eletrónico de Utentes",
                 font=("Arial", 14, "bold"), bg="#0d6efd", fg="white").pack()

        # Secção de Formulário (Registar)
        f_reg = tk.LabelFrame(self.root, text=" Registar Novo Utente ", font=("Arial", 10, "bold"),
                              bg="#f4f6f9", padx=15, pady=10)
        f_reg.pack(fill="x", padx=20, pady=10)

        tk.Label(f_reg, text="Nome Completo:", bg="#f4f6f9").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_nome = tk.Entry(f_reg, width=32, font=("Arial", 10))
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(f_reg, text="Telefone:", bg="#f4f6f9").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.entry_tel = tk.Entry(f_reg, width=15, font=("Arial", 10))
        self.entry_tel.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(f_reg, text="Guardar Utente", bg="#198754", fg="white", font=("Arial", 9, "bold"),
                  padx=10, command=self.registar_utente).grid(row=0, column=4, padx=15)

        # Secção de Pesquisa
        f_pesq = tk.Frame(self.root, bg="#f4f6f9", padx=20)
        f_pesq.pack(fill="x", pady=5)
        tk.Label(f_pesq, text="🔍 Pesquisar Utente:", bg="#f4f6f9", font=("Arial", 10)).pack(side="left")
        self.entry_pesquisa = tk.Entry(f_pesq, width=35, font=("Arial", 10))
        self.entry_pesquisa.pack(side="left", padx=10)
        self.entry_pesquisa.bind("<KeyRelease>", lambda e: self.atualizar_tabela())

        # Tabela (Treeview)
        f_tab = tk.Frame(self.root, padx=20, bg="#f4f6f9")
        f_tab.pack(fill="both", expand=True, pady=5)

        colunas = ("numero", "nome", "telefone", "consultas")
        self.tree = ttk.Treeview(f_tab, columns=colunas, show="headings", height=10)
        self.tree.heading("numero", text="N.º de Registo")
        self.tree.heading("nome", text="Nome Completo")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("consultas", text="Total de Consultas")

        self.tree.column("numero", width=150, anchor="center")
        self.tree.column("nome", width=280, anchor="w")
        self.tree.column("telefone", width=130, anchor="center")
        self.tree.column("consultas", width=130, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # Botão de Ação para a Ficha Clínica
        f_acoes = tk.Frame(self.root, bg="#f4f6f9", pady=10)
        f_acoes.pack()

        tk.Button(f_acoes, text="Abrir Ficha / Adicionar Consulta Clínica", bg="#0d6efd", fg="white",
                  font=("Arial", 10, "bold"), padx=15, pady=5, command=self.abrir_ficha_utente).pack()

        self.atualizar_tabela()

    def registar_utente(self):
        nome = self.entry_nome.get().strip()
        tel = self.entry_tel.get().strip()

        if not nome:
            messagebox.showwarning("Aviso", "O campo 'Nome Completo' é obrigatório!")
            return

        num_registo = f"SREU-2026-{len(self.utentes) + 1:03d}"
        novo_utente = {
            "numero": num_registo,
            "nome": nome,
            "telefone": tel if tel else "N/A",
            "consultas": []
        }

        self.utentes.append(novo_utente)
        self.guardar_dados()

        self.entry_nome.delete(0, tk.END)
        self.entry_tel.delete(0, tk.END)
        self.atualizar_tabela()
        messagebox.showinfo("Sucesso", f"Utente registado com sucesso!\nNúmero Único: {num_registo}")

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        termo = self.entry_pesquisa.get().lower()
        for u in self.utentes:
            if termo in u["nome"].lower() or termo in u["numero"].lower():
                self.tree.insert("", "end", values=(
                    u["numero"], u["nome"], u["telefone"], len(u["consultas"])
                ))

    def abrir_ficha_utente(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione primeiro um utente na tabela!")
            return

        num_registo = self.tree.item(selecionado[0], "values")[0]
        u = next((item for item in self.utentes if item["numero"] == num_registo), None)

        if not u:
            return

        # Janela Secundária para a Ficha do Utente
        janela = tk.Toplevel(self.root)
        janela.title(f"Ficha Clínica - {u['nome']}")
        janela.geometry("520x460")
        janela.configure(bg="#ffffff")

        tk.Label(janela, text=f"Utente: {u['nome']}", font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=(15, 2))
        tk.Label(janela, text=f"N.º de Registo: {u['numero']}  |  Telefone: {u['telefone']}",
                 font=("Arial", 10), fg="#666666", bg="#ffffff").pack(pady=(0, 10))

        tk.Label(janela, text="Registar Nova Observação / Consulta:", font=("Arial", 10, "bold"), bg="#ffffff").pack(
            anchor="w", padx=20)
        txt_obs = tk.Text(janela, height=4, width=55, font=("Arial", 9))
        txt_obs.pack(padx=20, pady=5)

        lista_historico = tk.Listbox(janela, width=65, height=8, font=("Arial", 9))

        def carregar_historico():
            lista_historico.delete(0, tk.END)
            for c in reversed(u["consultas"]):
                lista_historico.insert(tk.END, f"[{c['data']}] {c['observacao']}")

        def adicionar_observacao():
            obs = txt_obs.get("1.0", tk.END).strip()
            if not obs:
                messagebox.showwarning("Aviso", "Escreva a observação clínica.", parent=janela)
                return

            u["consultas"].append({
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "observacao": obs
            })
            self.guardar_dados()
            txt_obs.delete("1.0", tk.END)
            carregar_historico()
            self.atualizar_tabela()
            messagebox.showinfo("Sucesso", "Consulta adicionada ao histórico!", parent=janela)

        tk.Button(janela, text="Adicionar ao Histórico Clínico", bg="#198754", fg="white",
                  font=("Arial", 9, "bold"), command=adicionar_observacao).pack(pady=5)

        tk.Label(janela, text="Histórico de Consultas:", font=("Arial", 10, "bold"), bg="#ffffff").pack(anchor="w",
                                                                                                        padx=20,
                                                                                                        pady=(10, 0))
        lista_historico.pack(padx=20, pady=5)
        carregar_historico()


if __name__ == "__main__":
    root = tk.Tk()
    app = SREUGUI(root)
    root.mainloop()