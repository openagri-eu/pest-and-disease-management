import datetime

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

import crud
from api import deps
from schemas import Message, CreateData, UnitCreate
from crud import data

from csv import reader
from codecs import iterdecode

router = APIRouter()


@router.post("/upload/", response_model=Message)
async def upload(
        csv_file: UploadFile = File(...),
        db: Session = Depends(deps.get_db)
) -> Message:
    """
    Upload a .csv file (Using the ploutos .csv provided as how a baseline file should be formatted)
    """

    csv_reader = reader(iterdecode(csv_file.file, "utf-8-sig"), delimiter=";")
    first_column = True
    for row in csv_reader:
        if first_column:
            # Check against existing units, if new ones add them to db.
            for unit in row:
                parts = unit.split(" ")
                # Filter the first 4 cols
                if len(parts) == 1:
                    continue
                # This gets the wind direction out (because it has no unit)
                elif parts[-1].find(")") == -1:
                    continue
                unit_name = "".join(e + "_" for e in (parts[:len(parts)-1])).lower().strip("_")
                unit_db = crud.unit.get_by_name(db=db, name=unit_name)
                if unit_db:
                    continue
                # Check whether unit is already in db
                symbol_name = parts[-1].strip("()")

                print(unit_name)
                print(symbol_name)

                crud.unit.create(db=db, obj_in=UnitCreate(name=unit_name, symbol=symbol_name))

            first_column = False
            # return Message(message="lol")
            continue

        # return Message(message="kek")

        obj_in = CreateData(
            date=datetime.datetime.strptime(row[0], "%Y-%m-%d"),
            time=datetime.datetime.strptime(row[1], "%H:%M:%S").time(),
            nuts3=row[2],
            nuts2=row[3],
            temperature_air=float(row[4].replace(",", ".")) if row[4] != "" else None,
            relative_humidity=float(row[5].replace(",", ".")) if row[5] != "" else None,
            precipitation=float(row[6].replace(",", ".")) if row[6] != "" else None,
            wind_speed=float(row[7].replace(",", ".")) if row[7] != "" else None,
            wind_direction=float(row[8].replace(",", ".")) if row[8] != "" else None,
            wind_gust=float(row[9].replace(",", ".")) if row[9] != "" else None,
            atmospheric_pressure=float(row[10].replace(",", ".")) if row[10] != "" else None,
            relative_humidity_canopy=float(row[11].replace(",", ".")) if row[11] != "" else None,
            temperature_canopy=float(row[12].replace(",", ".")) if row[12] != "" else None,
            solar_irradiance_copernicus=float(row[13].replace(",", ".")) if row[13] != "" else None
        )
        data.create(db=db, obj_in=obj_in)

    return Message(message="Successfully uploaded file.")

    #     aggregate_str = ""
    #     for col in row:
    #         aggregate_str += col + ";"
    #
    #     temp = [ags for ags in aggregate_str.split(";") if ags != ""]
    #
    #     if len(temp) < 14:
    #         print("skipped row")
    #         continue
    #
    #     # NICE_TO_HAVE: Optimization: instead of doing a insert by insert, create a batch insert job for the db (1000 at a time)
    #
    #     # Parse .csv file
    #     obj_in = CreateData(
    #         date=datetime.datetime.strptime(temp[0], "%Y-%m-%d"),
    #         time=datetime.datetime.strptime(temp[1], "%H:%M:%S").time(),
    #         nuts3=temp[2],
    #         nuts2=temp[3],
    #         temperature_air=int(temp[4]),
    #         relative_humidity=int(temp[5]),
    #         precipitation=int(temp[6]),
    #         wind_speed=int(temp[7]),
    #         wind_direction=int(temp[8]),
    #         wind_gust=int(temp[9]),
    #         atmospheric_pressure=int(temp[10]),
    #         relative_humidity_canopy=int(temp[11]),
    #         temperature_canopy=int(temp[12]),
    #         solar_irradiance_copernicus=int(temp[13])
    #     )
    #     data.create(db=db, obj_in=obj_in)
    #
    # return Message(message="Successfully uploaded file.")
