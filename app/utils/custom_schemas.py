context = {
    "ocsm": "https://w3id.org/ocsm/",
    "fsm": "http://www.farmtopia.com/ontology/farmtopia#",
    "foodie": "http://foodie-cloud.com/model/foodie#",
    "saref": "https://saref.etsi.org/core/"
}

calculated_risk = {
    "@id": "urn:openagri:pestPrediction:{}", #uuid.uuid4()
    "@type": "fsm:PestInfestationRisk",
    "saref:hasTimestamp": "{}",
    "ocsm:hasRiskLevel": "{}" # Low, Medium, High
}