from fastapi  import FastAPI, Path, HTTPException, Query
import json 
from typing import Annotated ,Literal, Optional
from  pydantic import BaseModel , Field, computed_field
from fastapi.responses import JSONResponse

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description = 'ID of the patient', examples = ["P001"] )]
    name: Annotated[str, Field(..., description= "enter your name ")]
    city: Annotated[str, Field(..., description="enter the age")]
    age: Annotated[int , Field(..., gt=0, lt= 100, description="Age of  patient")]
    gender: Annotated[Literal["male", "Female", 'others'], Field(..., description = 'Gendre of the patient' )]
    height: Annotated[float, Field(..., gt = 0, description= "wait of the patient")]
    weight: Annotated[float, Field(..., gt= 0 , description= "enter your wait here")]
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self)-> str:
        if self.bmi <  18 :
            return "underweight"
        elif self.bmi <  25 :
            return "normal"
        elif self.bmi < 30  :
            return "overweight"
        else:
            return "Obese"
class Patient_update(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int] , Field(default=None)]
    gender: Annotated[Optional[Literal["male", "Female", 'others']], Field(default=None )]
    height: Annotated[Optional[float], Field(default=None )]
    weight: Annotated[Optional[float], Field(default=None) ]



def save_data(data):
    with open("patient.json",  "w") as f:
        json.dump(data , f)


    

def load_data():
    with open( "patient.json" , "r") as f :
        data = json.load(f)
        return data

@app.get("/")
def hello():
    return {"message"  : "patient  management   api"}

@app.get('/about')
def home():
    return {"message" : " a full function api tomanage your patient "}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def  view_patient(patient_id : str = Path( description = "thi is store in  db " , example = "P001")):
    data = load_data()
    if patient_id in data :
        return data[patient_id]
    
    raise HTTPException(status_code=400, detail= 'patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description ="sort on the basis of height  weight"), order: str = Query('asc', description= 'sort in asc or desc order' ) ):
    valid_field = ['height', 'weight', 'bmi']
    if sort_by not  in valid_field:
        raise HTTPException(status_code= 400, detail= 'invalid field select')
    if order not  in ['asc',"desc"]:
        raise HTTPException(status_code=400 ,detail='invalid order select between asc and  desc')
    data = load_data()
    sort_order = True if order == "desc" else False
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0) ,  reverse=sort_order)
    return sorted_data

@app.post('/create')
def creat_patient(patient: Patient):
    data = load_data()
    if patient.id in data :
        raise HTTPException(status_code=400, detail="patient id exist")
    
    data[patient.id] = patient.model_dump(exclude= ["id"])
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "patient is created"})

@app.put('/update_info' )
def update_information(patient_id: str , patient_update: Patient_update):
    data = load_data()

    if patient_id not in  data:
        raise HTTPException(status_code= 404, detail= "patient not found")
    

    existing_info = data[patient_id]
    updating_info = patient_update.model_dump(exclude_unset = True)

    for key, value in updating_info.items():
      existing_info[key] = value
    


    patient_pydantic_object = Patient(
    id=patient_id,
    name=existing_info["name"],
    city=existing_info["city"],
    age=existing_info["age"],
    gender=existing_info["gender"],
    height=existing_info["height"],
    weight=existing_info["weight"]
)
    new_info = patient_pydantic_object.model_dump(exclude= {"id"})

    data[patient_id] = new_info
    print(data)
    save_data(data)
    return {"message": "data saved succesfully"}
        


@app.delete('/delete/{patient_id}')
def delete_id(patient_id: str):
    data = load_data()
    if patient_id not in data :
        return JSONResponse(status_code=200 , content= {'message': "patient delet"})
    
    del data[patient_id]
    save_data(data)
