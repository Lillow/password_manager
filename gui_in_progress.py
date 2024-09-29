import tkinter as tk
from tkinter import Grid, messagebox, ttk
from manager.password_manager import PasswordManager
from manager.password import Password, PasswordFilter

manager: PasswordManager = PasswordManager()


def add_password() -> None:
    category: str = entry_category.get()
    description: str = entry_description.get()
    login: str = entry_login.get()
    password: str = entry_password.get()

    if category and description and password:
        password = Password(
            category=category,
            description=description,
            login=login,
            password=password,
        )
        manager.add_password(password=password)
        messagebox.showinfo("Success", "Password added successfully!")
        clear_entries()


############################################################################


def search_passwords() -> None:
    for row in tree.get_children():
        tree.delete(row)

    results: list[Password] = manager.get_password()

    for row in results:
        tree.insert(
            "",
            "end",
            values=(
                row.id,
                row.category,
                row.description,
                row.login,
                row.password,
            ),
        )


############################################################################


def delete_password() -> None:
    selected_item: tuple[str, ...] = tree.selection()  # Obter a linha selecionada
    if selected_item:
        password_id = tree.item(selected_item[0], "values")[
            0
        ]  # Pegar o ID da senha selecionada
        manager.del_password(password_id)  # Chama o método para deletar a senha
        messagebox.showinfo("Sucesso", "Senha deletada com sucesso!")
        search_passwords()  # Atualizar a tabela com as informações
    else:
        messagebox.showwarning("Erro", "Selecione uma senha para deletar.")


############################################################################


def update_password():
    selected_item: tuple[str, ...] = tree.selection()
    password_id = ''
    if selected_item:
        password_id = tree.item(selected_item[0], "values")[
            0
        ]  # Pegar o ID da senha selecionada
    category = entry_category.get()
    description = entry_description.get()
    login = entry_login.get()
    password = entry_password.get()
    selected_item: tuple[str, ...] = tree.selection()  # Obter a linha selecionada
    new_password = Password(category, description, login, password)

    if password_id and category and description and password:
        manager.upd_password(password_id, new_password)
        messagebox.showinfo("Sucesso", "Senha atualizada com sucesso!")
        search_passwords()  # Atualizar a tabela com as novas informações
    else:
        messagebox.showwarning("Erro", "Preencha todos os campos obrigatórios!")


############################################################################


def clear_entries() -> None:
    entry_category.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    entry_login.delete(0, tk.END)
    entry_password.delete(0, tk.END)


############################################################################

root = tk.Tk()
root.title("Password Manager")

tk.Label(root, text="Category").grid(row=0, column=0, padx=10, pady=10)
entry_category = tk.Entry(root)
entry_category.grid(row=0, column=1)

tk.Label(root, text="Description").grid(row=1, column=0, padx=10, pady=10)
entry_description = tk.Entry(root)
entry_description.grid(row=1, column=1)

tk.Label(root, text="Login").grid(row=2, column=0, padx=10, pady=10)
entry_login = tk.Entry(root)
entry_login.grid(row=2, column=1)

tk.Label(root, text="Password").grid(row=3, column=0, padx=10, pady=10)
entry_password = tk.Entry(root)
entry_password.grid(row=3, column=1)

############################################################################

bnt_add = tk.Button(root, text="Add Password", command=add_password)
bnt_add.grid(row=4, column=0, columnspan=2, pady=10)

############################################################################

columns = ("ID", "Category", "Description", "Login", "Password")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

btn_search = tk.Button(root, text="Search Passwords", command=search_passwords)
btn_search.grid(row=6, column=0, columnspan=2, pady=10)

# Botão para deletar a senha selecionada
btn_delete = tk.Button(root, text="Delete", command=delete_password)
btn_delete.grid(row=6, column=1, columnspan=2, pady=10)


btn_update = tk.Button(root, text="Update Password", command=update_password)
btn_update.grid(row=7, column=0, columnspan=2, pady=10)

############################################################################
if __name__ == "__main__":
    root.mainloop()
