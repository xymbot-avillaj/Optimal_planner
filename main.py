from fastapi import FastAPI
from libraries.entities import EntityUpdateNotification, OPEEntity
import libraries.optimal_planner as op
import os
import requests
import socket


def init ():
    op.ORION_URL = os.getenv('ORION')
    url_noti="http://"+str(socket.gethostname())+":8000/updates"
    noti = {'id':'urn:ngsi:OP_notification:001','description': 'Notify me when Optimal planner entity arrive', 'subject': {'entities':[{'idPattern':'.*','type': 'Optimal_Planner_init'}]},'notification':{'http':{'url':'{0}'.format(url_noti)}}}
    try:
        print(op.postResult(op.ORION_URL + '/v2/subscriptions', noti, {'Content-Type': 'application/json',}))
    except requests.exceptions.ConnectionError:
        print('Unable to stablish connection to FIWARE-Orion {0} for entity creation. Please, contact the developer team '.format(op.ORION_URL))
        return


def plan_order(ms: [OPEEntity]):
    for m in ms:  # TODO zap
        print(m)
        op.ini(m.Operators,m.Orders,m.Production)
        op.optimization()

VERSION = '1.0.0'

init()

app = FastAPI()


@app.get('/')
def read_root():
    return {'optimal planner': VERSION}


@app.get("/version")
def read_version():
    return read_root()


@app.post("/updates")
def post_updates(notification: EntityUpdateNotification):
    updated_plan = notification.filter_entities(OPEEntity)
    plan_order(updated_plan)
    return 0
