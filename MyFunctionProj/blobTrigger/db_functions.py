import ast

def load_info(conn, info, title):

    cursor = conn.cursor(dictionary=True)
    values = (info, title)
    request = """
    UPDATE library
    SET info = %s
    WHERE titre = %s
    """
    cursor.execute(request, values)
    conn.commit()
