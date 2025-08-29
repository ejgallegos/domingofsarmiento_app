# file: controllers/socio_controller.py

from tkinter import messagebox
from models.socio_model import SocioModel
# Aquí importarías la ventana de diálogo para añadir/editar, que sería otra Vista.
# from views.socio_dialog_view import SocioDialogView 

class SocioController:
    def __init__(self, view):
        self.view = view
        self.model = SocioModel()

    def load_initial_data(self):
        """ Carga los datos iniciales en la vista. """
        socios = self.model.get_all_socios()
        self.view.update_treeview(socios)
        
    def search_socios(self, event=None):
        """ Busca socios según el término de búsqueda de la vista. """
        search_term = self.view.get_search_term()
        socios = self.model.get_all_socios(search_term)
        self.view.update_treeview(socios)
        
    def delete_socio(self):
        """ Elimina el socio seleccionado en la vista. """
        socio_id = self.view.get_selected_socio_id()
        if not socio_id:
            messagebox.showwarning("Atención", "Por favor, seleccione un socio para eliminar.")
            return

        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar al socio con ID {socio_id}?"):
            if self.model.delete_socio(socio_id):
                messagebox.showinfo("Éxito", "Socio eliminado correctamente.")
                self.search_socios() # Refresca la lista
            else:
                messagebox.showerror("Error", "No se pudo eliminar el socio.")
                
    def show_add_socio_dialog(self):
        # Aquí crearías una ventana Toplevel (que sería otra clase de Vista)
        # y le pasarías una función de este controlador para el guardado.
        messagebox.showinfo("TODO", "Implementar diálogo para agregar nuevo socio.")
        # Ejemplo:
        # dialog = SocioDialogView(self.view, "Nuevo Socio", self.save_new_socio)
        # self.view.wait_window(dialog)
        
    def show_edit_socio_dialog(self):
        socio_id = self.view.get_selected_socio_id()
        if not socio_id:
            messagebox.showwarning("Atención", "Por favor, seleccione un socio para modificar.")
            return
        messagebox.showinfo("TODO", f"Implementar diálogo para editar socio con ID {socio_id}.")
        # Lógica similar: obtener datos del socio con el model, pasarlos al dialog,
        # y tener una función en este controlador para guardar los cambios.