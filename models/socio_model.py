# file: models/socio_model.py

from database.database_manager import DatabaseManager

class SocioModel:
    def get_all_socios(self, search_term=""):
        """ Obtiene todos los socios o los filtra por un término de búsqueda. """
        query = """
            SELECT Id_socio, dni, apellidos, nombres, telefono, direccion, estado, prestamos_activos 
            FROM Socios 
            WHERE apellidos LIKE ? OR nombres LIKE ?
            ORDER BY apellidos
        """
        like_term = f"%{search_term}%"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (like_term, like_term))
                return cursor.fetchall()
        return []

    def add_socio(self, socio_data):
        """ Agrega un nuevo socio a la base de datos. """
        query = "INSERT INTO Socios (Id_socio, dni, apellidos, nombres, telefono, direccion, estado, prestamos_activos) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, socio_data)
                return True
        return False

    def update_socio(self, socio_data):
        """ Actualiza un socio existente. """
        query = """
            UPDATE Socios 
            SET apellidos=?, nombres=?, telefono=?, direccion=?, estado=?, prestamos_activos=? 
            WHERE dni=?
        """
        # Reordenamos los datos para que coincidan con la consulta
        data_for_update = (
            socio_data['apellidos'], socio_data['nombres'], socio_data['telefono'],
            socio_data['direccion'], socio_data['estado'], socio_data['prestamos_activos'],
            socio_data['dni'] 
        )
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, data_for_update)
                return True
        return False

    def delete_socio(self, socio_id):
        """ Elimina un socio por su ID. """
        query = "DELETE FROM Socios WHERE Id_socio = ?"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (socio_id,))
                return True
        return False

    def get_next_id(self):
        """ Obtiene el siguiente ID correlativo para un nuevo socio. """
        query = "SELECT MAX(Id_socio) FROM Socios"
        with DatabaseManager() as cursor:
            if cursor:
                result = cursor.execute(query).fetchone()
                return (result[0] or 0) + 1
        return 1