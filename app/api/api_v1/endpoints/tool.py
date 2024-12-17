from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import utils
from api import deps
from models import User
from schemas import list_path_param, DatasetIds

import crud


router = APIRouter()


@router.get("/calculate-risk-index/weather/{weather_dataset_id}/model/{model_ids}/verbose/")
def calculate_risk_index_verbose(
    weather_dataset_id: int,
    model_ids: DatasetIds = Depends(list_path_param),
    db: Session = Depends(deps.get_db),
    user: User = Depends(deps.get_current_user)
):
    """
    Calculates the risk index for some dataset x (weather data for a parcel), using pest models (y,z,...)
    The risk is calculated by assigning the rule that is valid for a weather datapoint
    """

    # Check ids
    dataset_db = crud.dataset.get(db=db, id=weather_dataset_id)

    if not dataset_db:
        raise HTTPException(
            status_code=400,
            detail="Error, dataset with ID:{} does not exist".format(weather_dataset_id)
        )

    pest_models = []

    for mid in model_ids.ids:
        pest_model_db = crud.pest_model.get(db=db, id=mid)

        if not pest_model_db:
            raise HTTPException(
                status_code=400,
                detail="Error, pest model with ID:{} does not exist".format(mid)
            )

        pest_models.append(pest_model_db)

    calculations = utils.calculate_risk_index_probability(db=db, weather_dataset_id=weather_dataset_id, pest_models=pest_models)

    return calculations

@router.get("/calculate-risk-index/weather/{weather_dataset_id}/model/{model_ids}/high/")
def calculate_risk_index_high(
    weather_dataset_id: int,
    model_ids: DatasetIds = Depends(list_path_param),
    db: Session = Depends(deps.get_db),
    user: User = Depends(deps.get_current_user)
):
    """
    Calculates the risk index for some dataset x (weather data for a parcel), using pest models (y,z,...)
    The risk is calculated by assigning the rule that is valid for a weather datapoint
    This API only returns "High" risk datapoints
    """

    # Check ids
    dataset_db = crud.dataset.get(db=db, id=weather_dataset_id)

    if not dataset_db:
        raise HTTPException(
            status_code=400,
            detail="Error, dataset with ID:{} does not exist".format(weather_dataset_id)
        )

    pest_models = []

    for mid in model_ids.ids:
        pest_model_db = crud.pest_model.get(db=db, id=mid)

        if not pest_model_db:
            raise HTTPException(
                status_code=400,
                detail="Error, pest model with ID:{} does not exist".format(mid)
            )

        pest_models.append(pest_model_db)

    calculations = utils.calculate_risk_index_probability(db=db, weather_dataset_id=weather_dataset_id, pest_models=pest_models, parameter="High")

    return calculations
