# file: models/libro_model.py

from database.database_manager import DatabaseManager

class LibroModel:
    def get_all_libros(self, search_term=""):
        """ Obtiene todos los libros o los filtra por título o autor. """
        query = """
            SELECT Id_libro, titulo, autor, isbn, editorial, año, cantidad, categoria 
            FROM Libros 
            WHERE titulo LIKE ? OR autor LIKE ?
            ORDER BY titulo
        """
        like_term = f"%{search_term}%"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (like_term, like_term))
                return cursor.fetchall()
        return []

    def add_libro(self, libro_data):
        """ Agrega un nuevo libro a la base de datos. """
        query = "INSERT INTO Libros (Id_libro, titulo, autor, isbn, editorial, año, cantidad, categoria) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, libro_data)
                return True
        return False

    def update_libro(self, libro_data):
        """ Actualiza un libro existente. """
        query = """
            UPDATE Libros 
            SET titulo=?, autor=?, isbn=?, editorial=?, año=?, cantidad=?, categoria=? 
            WHERE Id_libro=?
        """
        data_for_update = (
            libro_data['titulo'], libro_data['autor'], libro_data['isbn'],
            libro_data['editorial'], libro_data['año'], libro_data['cantidad'],
            libro_data['categoria'], libro_data['id']
        )
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, data_for_update)
                return True
        return False

    def delete_libro(self, libro_id):
        """ Elimina un libro por su ID. """
        query = "DELETE FROM Libros WHERE Id_libro = ?"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (libro_id,))
                return True
        return False

    def get_next_id(self):
        """ Obtiene el siguiente ID correlativo para un nuevo libro. """
        query = "SELECT MAX(Id_libro) FROM Libros"
        with DatabaseManager() as cursor:
            if cursor:
                result = cursor.execute(query).fetchone()
                return (result[0] or 0) + 1
        return 1