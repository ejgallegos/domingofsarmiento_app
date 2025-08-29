# file: controllers/libro_controller.py

from tkinter import messagebox
from models.libro_model import LibroModel

class LibroController:
    def __init__(self, view):
        self.view = view
        self.model = LibroModel()

    def load_initial_data(self):
        libros = self.model.get_all_libros()
        self.view.update_treeview(libros)
        
    def search_libros(self, event=None):
        search_term = self.view.get_search_term()
        libros = self.model.get_all_libros(search_term)
        self.view.update_treeview(libros)
        
    def delete_libro(self):
        libro_id = self.view.get_selected_libro_id()
        if not libro_id:
            messagebox.showwarning("Atención", "Por favor, seleccione un libro para eliminar.")
            return

        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el libro con ID {libro_id}?"):
            if self.model.delete_libro(libro_id):
                messagebox.showinfo("Éxito", "Libro eliminado correctamente.")
                self.search_libros()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el libro.")
                
    def show_add_libro_dialog(self):
        messagebox.showinfo("TODO", "Implementar diálogo para agregar nuevo libro.")
        
    def show_edit_libro_dialog(self):
        libro_id = self.view.get_selected_libro_id()
        if not libro_id:
            messagebox.showwarning("Atención", "Por favor, seleccione un libro para modificar.")
            return
        messagebox.showinfo("TODO", f"Implementar diálogo para editar libro con ID {libro_id}.")