from celery import Celery
import mysql.connector


app = Celery('celery_app')
app.conf.broker_url = 'redis://localhost:6379/0'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls updateBlocks() every 30 seconds.
    sender.add_periodic_task(30.0, updateBlocks.s(), name='update blocks since lastupdate')


@app.task
def updateBlocks():
    print('connecting to mysql DB')
    cnx = mysql.connector.connect(user='lcherukuri', password='Phani_3008',
                                  host='127.0.0.1', database='test',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("SELECT * FROM example")
    cursor.execute(query)
    for record in cursor:
        print(record)
    print('closing connection')
    cnx.close()
