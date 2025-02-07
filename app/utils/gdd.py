import datetime
from typing import List

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

import crud
from models import Parcel, Disease
from schemas import DiseaseModel, GDDResponseChunk


def calculate_gdd(db: Session, parcel: Parcel, disease_models: List[Disease],
                  start: datetime.date, end: datetime.date) -> List[DiseaseModel]:

    # SQL query for the data
    data_db = crud.data.get_data_query_by_parcel_id_and_date_interval(db=db, parcel_id=parcel.id,
                                                                      date_from=start, date_to=end)

    df = pd.read_sql(sql=data_db.statement, con=db.bind, parse_dates={"date": "%Y-%m-%d"})


    df['datetime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str))

    #swap cols
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    df = df.drop(["date", "time", "id"], axis=1)
    df = df.drop(["atmospheric_temperature_daily_min", "atmospheric_temperature_daily_max", "atmospheric_temperature_daily_average",
                  "atmospheric_relative_humidity", "atmospheric_pressure", "precipitation", "average_wind_speed", "wind_direction",
                  "wind_gust", "leaf_relative_humidity", "leaf_temperature", "leaf_wetness", "soil_temperature_10cm", "soil_temperature_20cm",
                  "soil_temperature_30cm", "soil_temperature_40cm", "soil_temperature_50cm", "soil_temperature_60cm", "solar_irradiance_copernicus",
                  "parcel_id"], axis=1)

    df = df.resample("1D", on="datetime").mean()

    df["atmospheric_temperature"] = df["atmospheric_temperature"].apply(np.ceil)

    disease_model_list = []

    for disease_model in disease_models:

        gdd_values = []
        acc_value = 0

        for row in df.itertuples():
            date = row[0].date()
            avg_temp = row[1]

            gdd_to_add = 0
            if avg_temp > disease_model.base_gdd:
                gdd_to_add = avg_temp - disease_model.base_gdd

            acc_value += gdd_to_add

            # Find which descriptor should this gdd chunk take
            descriptor = "No defined descriptor for this amount of gdd"
            for interval in disease_model.gdd_points:
                if acc_value not in range(interval.start, interval.end):
                    continue

                descriptor = interval.descriptor

            gdd_values.append(
                GDDResponseChunk(
                    date=date,
                    gdd_value=gdd_to_add,
                    accumulated_gdd=acc_value,
                    descriptor=descriptor
                )
            )

        response_obj = DiseaseModel(
            name=disease_model.name,
            eppo_code=disease_model.eppo_code,
            base_gdd=disease_model.base_gdd,
            description=disease_model.description,
            gdd_values=gdd_values
        )

        disease_model_list.append(response_obj)

    return disease_model_list
