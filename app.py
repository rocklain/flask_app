from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()






@app.errorhandler(403)
def error_403(error):
    return render_template('error_pages/403.html'), 403

@app.errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)