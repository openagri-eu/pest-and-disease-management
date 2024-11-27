from typing import List, Optional

from sqlalchemy.orm import Session
import pandas as pd

import crud
import utils
import uuid

from models import PestModel


def calculate_risk_index_probability(db: Session, weather_dataset_id: int, pest_models: List[PestModel], parameter: Optional[str] = None):
    # SQL query for the data
    data_db = crud.data.get_data_query_by_dataset_id(db=db, dataset_id=weather_dataset_id)

    dataset_db = crud.dataset.get(db=db, id=weather_dataset_id)

    df = pd.read_sql(sql=data_db.statement, con=db.bind, parse_dates={"date": "%Y-%m-%d"})

    # Calculate the risks associated with each pest_model
    for pm in pest_models:
        risks_for_current_pm = ["Low"] * df.shape[0]

        for rule in pm.rules:
            final_str = "(x['{}'] {} {})".format(rule.conditions[0].unit.name, rule.conditions[0].operator.symbol, float(rule.conditions[0].value))
            for cond in rule.conditions[1:]:
                final_str = final_str + " & " + "(x['{}'] {} {})".format(cond.unit.name, cond.operator.symbol, float(cond.value))

            df_with_risk = df.assign(risk=eval("lambda x: {}".format(final_str)))

            # With this, only one rule should only ever fire for one singular date/time weather data point.
            # If multiple rules turn up as valid (both are true), then the last one from the db is going to have its
            # prob. value written as a final response for this pest model
            risks_for_current_pm = [rule.probability_value if x else y for x, y in zip(df_with_risk["risk"], risks_for_current_pm)]

        df["{}".format(pm.name)] = risks_for_current_pm

    context = utils.context

    graph = []

    for pm in pest_models:

        calculated_risks = []
        for date, time, risk in zip(df["date"], df["time"], df["{}".format(pm.name)]):

            if parameter and risk != parameter:
                continue

            calculated_risks.append(
                {
                    "@id": "urn:openagri:pestInfectationRisk:obs2:{}".format(uuid.uuid4()),
                    "@type": ["Observation", "PestInfestationRisk"],
                    "phenomenonTime": "{}".format(str(date).split(" ")[0] + "T" + str(time)),
                    "hasSimpleResult": "{}".format(risk)
                }
            )

        graph_element = {
            "@id": "urn:openagri:pestInfectationRisk:{}".format(uuid.uuid4()),
            "@type": ["ObservationCollection"],
            "description": "{} pest infectation risk forecast in x ".format(pm.name),
            "observedProperty": {
                "@id": "urn:openagri:pestInfectationRisk:op:{}".format(uuid.uuid4()),
                "@type": ["ObservableProperty", "PestInfection"],
                "name": "UNCINE pest infection",
                "hasAgriPest": {
                    "@id": "urn:openagri:pest:UNCINE",
                    "@type": "AgriPest",
                    "name": "UNCINE",
                    "description": "Uncinula necator (syn. Erysiphe necator) is a fungus that causes powdery mildew of grape. It is a common pathogen of Vitis species, including the wine grape, Vitis vinifera",
                    "eppoConcept": "https://gd.eppo.int/taxon/UNCINE"
                }
            },
            "madeBySensor": {
                "@id": "urn:openagri:pestInfectationRisk:model:{}".format(uuid.uuid4()),
                "@type": ["Sensor", "AIPestDetectionModel"],
                "name": "AI pest detaction model xyz"
            },
            "hasFeatureOfInterest": {
                "@id": "urn:openagri:pestInfectationRisk:foi:{}".format(uuid.uuid4()),
                "@type": ["FeatureOfInterest", "Point"],
                "long": 39.1436719643054,
                "lat": 27.40518186700786
            },
            "basedOnWeatherDataset": {
                "@id": "urn:openagri:weatherDataset:{}".format(weather_dataset_id),
                "@type": "WeatherDataset",
                "name": "{}".format(dataset_db.name)
            },
            "resultTime": "2024-10-01T12:00:00+00:00",
            "hasMember": calculated_risks
        }

        graph.append(graph_element)

    doc = {
        "@context": context,
        "@graph": graph
    }

    return doc
