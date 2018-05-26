from celery import Celery

app = Celery('celery_app')
app.conf.broker_url = 'redis://localhost:6379/0'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls updateBlocks() every 30 seconds.
    sender.add_periodic_task(30.0, updateBlocks.s(), name='update blocks since lastupdate')


@app.task
def updateBlocks():
    print("Updating Blocks")
