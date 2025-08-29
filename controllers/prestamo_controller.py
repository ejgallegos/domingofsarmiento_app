# file: controllers/prestamo_controller.py

from tkinter import messagebox
from models.prestamo_model import PrestamoModel

class PrestamoController:
    def __init__(self, view):
        self.view = view
        self.model = PrestamoModel()

    def load_initial_data(self):
        prestamos = self.model.get_all_prestamos()
        self.view.update_treeview(prestamos)

    def search_prestamos(self, event=None):
        search_term = self.view.get_search_term()
        prestamos = self.model.get_all_prestamos(search_term)
        self.view.update_treeview(prestamos)

    def devolver_prestamo(self):
        selected = self.view.get_selected_prestamo()
        if not selected:
            messagebox.showwarning("Atención", "Por favor, seleccione un préstamo para devolver.")
            return
            
        if selected['estado'] == 'Devuelto':
            messagebox.showinfo("Información", "Este préstamo ya ha sido devuelto.")
            return

        prestamo_id = selected['id']
        if messagebox.askyesno("Confirmar Devolución", f"¿Confirma la devolución del préstamo ID {prestamo_id}?"):
            if self.model.devolver_prestamo(prestamo_id):
                messagebox.showinfo("Éxito", "Préstamo devuelto correctamente.")
                self.search_prestamos()
            else:
                messagebox.showerror("Error", "Ocurrió un error al procesar la devolución.")

    def show_create_prestamo_dialog(self):
        messagebox.showinfo("TODO", "Implementar diálogo para crear préstamo.")

    def show_edit_prestamo_dialog(self):
        selected = self.view.get_selected_prestamo()
        if not selected:
            messagebox.showwarning("Atención", "Por favor, seleccione un préstamo para modificar.")
            return
        messagebox.showinfo("TODO", f"Implementar diálogo para modificar préstamo ID {selected['id']}.")