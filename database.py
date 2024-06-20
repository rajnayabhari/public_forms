import psycopg2
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    return psycopg2.connect(
    #for local
        # database="digi_muni",
        # user="postgres",
        # password="@hybesty123",
        # host="127.0.0.1",
        # port=5432
        
        #for render.com
        
        database="digi_muni",
        user="digi_muni_user",
        password="52ODMHwZil8AUVUFP2uOl13ZtiHtJz8j",
        host="dpg-cpo891bv2p9s73fruoag-a",
        port="5432"
    )
def database():
    
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS information (
            Id_no SERIAL PRIMARY KEY NOT NULL,
            Certificate_no VARCHAR(250) NOT NULL,
            fullname VARCHAR(250) NOT NULL,
            mothername VARCHAR(250) NOT NULL,
            fathername VARCHAR(250) NOT NULL,
            grandfathername VARCHAR(250) NOT NULL,
            dob VARCHAR(250) NOT NULL,
            gender VARCHAR(250) NOT NULL,
            issueddate VARCHAR(250) NOT NULL,
            education VARCHAR(250) NOT NULL,
            employeed VARCHAR(250) NOT NULL,
            abroad VARCHAR(250) NOT NULL,
            reason_for_unemployment VARCHAR(250) DEFAULT '0',
            reason_for_uneducated VARCHAR(250) DEFAULT '0',
            reason_for_abroad VARCHAR(250) DEFAULT '0',
            USER_ID INT NOT NULL,
            FOREIGN KEY (USER_ID) REFERENCES login (USER_ID)
            );
            """)
            
            
        conn.commit()