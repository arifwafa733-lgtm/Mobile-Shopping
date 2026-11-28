import oracledb

def get_connection():
    return oracledb.connect(
        user="arif",
        password="arif123",
        dsn="localhost:1521/ORCLPDB"
    )