# file: models/prestamo_model.py

from database.database_manager import DatabaseManager

class PrestamoModel:
    def get_all_prestamos(self, search_term=""):
        """ Obtiene todos los préstamos con información del socio y los libros. """
        query = """
            SELECT p.id_prestamo, p.fecha_retiro, p.fecha_devolucion,
                   (s.nombres || ' ' || s.apellidos) AS socio,
                   GROUP_CONCAT(l.titulo, ', ') AS libros,
                   p.estado
            FROM prestamos p
            JOIN socios s ON p.id_socio = s.id_socio
            JOIN prestamos_libros pl ON p.id_prestamo = pl.id_prestamo
            JOIN libros l ON pl.id_libro = l.id_libro
            WHERE socio LIKE ? OR libros LIKE ? OR p.estado LIKE ?
            GROUP BY p.id_prestamo
            ORDER BY p.id_prestamo DESC
        """
        like_term = f"%{search_term}%"
        with DatabaseManager() as cursor:
            if cursor:
                cursor.execute(query, (like_term, like_term, like_term))
                return cursor.fetchall()
        return []

    def devolver_prestamo(self, prestamo_id):
        """ Marca un préstamo como devuelto y actualiza el stock de libros y el estado del socio. """
        try:
            with sqlite3.connect("biblioteca.db") as conn: # Usamos conexión directa para manejar la transacción
                cursor = conn.cursor()
                
                # 1. Obtener los IDs de libros y socio asociados
                cursor.execute("SELECT id_socio FROM prestamos WHERE id_prestamo = ?", (prestamo_id,))
                id_socio = cursor.fetchone()[0]
                
                cursor.execute("SELECT id_libro FROM prestamos_libros WHERE id_prestamo = ?", (prestamo_id,))
                libros_ids = [row[0] for row in cursor.fetchall()]
                
                # Inicia transacción
                # 2. Actualizar estado del préstamo
                cursor.execute("UPDATE prestamos SET estado = 'Devuelto' WHERE id_prestamo = ?", (prestamo_id,))
                
                # 3. Incrementar stock de libros
                for libro_id in libros_ids:
                    cursor.execute("UPDATE Libros SET cantidad = cantidad + 1 WHERE Id_libro = ?", (libro_id,))
                
                # 4. Actualizar estado del socio
                cursor.execute("UPDATE Socios SET prestamos_activos = 0 WHERE id_socio = ?", (id_socio,))
                
                conn.commit() # Confirma todos los cambios
                return True
        except sqlite3.Error:
            # Si algo falla, la transacción no se confirma.
            return False

    # Las funciones para crear y modificar préstamos son más complejas y requieren diálogos
    # para seleccionar socios y libros. Las dejaremos como TODO en el controlador.