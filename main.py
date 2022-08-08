import uvicorn
from fastapi import FastAPI, Body, Depends, HTTPException,Header
import schemas, models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
import logging

app = FastAPI()

Base.metadata.create_all(engine)

fake_secret_token = "coneofsilence"

fake_db = {
    "vessel": {"name": "foo", "id": "Foo", "naccsCode": "There goes my hero","date": "10","destination": "ASDF"},
          }
          
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

'''Works only if you run uvicorn main:app --reload'''
logging.basicConfig(level=logging.DEBUG,filename="config.log",filemode="w",format="%(asctime)s-%(levelname)s-%(message)s")

@app.get("/")
async def get_vessels(session: Session = Depends(get_session)):
    try:
        vessels = session.query(models.Vessel).all()
        logging.info("The list of vessels")
        return vessels
    except NoResultFound:
        logging.exception("Exception")
        return None

@app.get("/destination/{destination}")
async def get_vessel(destination:str, session: Session = Depends(get_session)):
    try:
        logging.info(f"The vessel by current route '{destination}'")
        return session.query(models.Vessel).filter(models.Vessel.destination==destination).first()
    except NoResultFound:
        if destination not in fake_db:
            raise HTTPException(status_code=404, detail="Vessel not found")
        logging.exception("Exception")
        return None

@app.get("/date/{date}")
async def get_vessel(date:str, session: Session = Depends(get_session),x_token: str = Header()):
    try:
        if x_token != fake_secret_token:
            raise HTTPException(status_code=400, detail="Invalid X-Token header")
        logging.info(f"The vessel by typed date '{date}'")
        return session.query(models.Vessel).filter(models.Vessel.date==date).first()
    except NoResultFound:
        logging.exception("The vessel by typed date not found")
        return None

@app.post("/add/")
async def add_vessel(vessel:schemas.Vessel, session: Session = Depends(get_session)):
    vessel = models.Vessel(name=vessel.name, id=vessel.id, naccsCode=vessel.naccsCode, date=vessel.date,destination=vessel.destination)
    try:
        session.add(vessel)
        session.commit()
        session.refresh(vessel)
        logging.info(f"The vessel with fileds'name:{vessel.name}, id:{vessel.id}, naccsCode:{vessel.naccsCode}, date:{vessel.date}, destination:{vessel.destination}' is added")
    except Exception as error:
        logging.exception("Current NACCS code already exist")
        vessel = "Error: current NACCS code already exist"
    return vessel

@app.put("/update/{naccsCode}")
async def update_vessel(naccsCode:str, vessel:schemas.Vessel, session: Session = Depends(get_session)):
        vesselObject = session.query(models.Vessel).get(naccsCode)
        vesselObject.name=vessel.name
        vesselObject.id=vessel.id
        vesselObject.date=vessel.date
        vesselObject.destination=vessel.destination
        try:
             vesselObject.naccsCode=vessel.naccsCode
             session.commit()
             logging.info("The vessel is updated")
        except Exception as error:
            logging.exception("Typed NACCS code already exist, please enter unique value")
            vesselObject="Error: typed NACCS code already exist, please enter unique value"
        return vesselObject