from fastapi import FastAPI
from libraries.entities import EntityUpdateNotification, OPEEntity
import libraries.optimal_planner as op


def plan_order(ms: [OPEEntity]):
    for m in ms:  # TODO zap
        print(m)
        op.ini()
        op.optimization(m.Operators,m.Orders)

VERSION = '1.0.0'

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
