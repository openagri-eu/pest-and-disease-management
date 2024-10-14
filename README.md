# pest-and-disease-management

# Description

The Pest and Disease Management service takes in data via datasets or live measurements and rules created\
by a user, and returns when a rule was satisfied on the specified dataset.

# Requirements

<ul>
    <li>git</li>
    <li>docker</li>
    <li>docker-compose</li>
</ul>

Docker version used during development: 27.0.3

# Installation

There are two ways to install this service, via docker or directly from source.

<h3> Deploying from source </h3>

When deploying from source, use python 3:11.\
Also, you should use a [venv](https://peps.python.org/pep-0405/) when doing this.

A list of libraries that are required for this service is present in the "requirements.txt" file.\
This service uses FastAPI as a web framework to serve APIs, alembic for database migrations sqlalchemy for database ORM mapping.

<h3> Deploying via docker </h3>

After installing <code> docker </code> you can run the following commands to run the application:

```
docker compose build
docker compose up
```

The application will be served on http://127.0.0.1:80 (I.E. typing localhost/docs in your browser will load the swagger documentation)

# Documentation

Examples:

<h3> POST </h3>

```
/api/v1/data/upload/
```

Example Response:
```
{
    "msg": "Successfully uploaded file."
}
```

<h3> POST </h3>

```
/api/v1/rule/
```

Example Response:
```
{
    "id": 1,
    "name": "my_rule",
    "description": "explanation",
    "from_time": "12:30:00.000Z",
    "to_time": "08:45:00.000Z",
    "conditions": [
        {
            "unit_id": 1,
            "operator_id": 1,
            "value": 51
        },
        {
            "unit_id": 2,
            "operator_id": 2,
            "value": 12
        }
    ]
}
```

<h3> GET </h3>

```
/api/v1/tool/calculate-risk-index/{rule_id}
```

Example Response:
```
{
    "rule": {
        "id": 1,
        "name": "my_rule",
        "description": "explanation",
        "from_time": "12:30:00.000Z",
        "to_time": "08:45:00.000Z",
        "conditions": [
            {
                "unit_id": 1,
                "operator_id": 1,
                "value": 51
            },
            {
                "unit_id": 2,
                "operator_id": 2,
                "value": 12
            }
        ]
    },
    "risk_index_per_day": [
        {
            "date": 2022-01-01,
            "risk_index": 20
        },
        
    ]
}
```

<h3> Example usage </h3>

In order to obtain the days when a rule was satisfied, you need to define a rule and upload a dataset upon which to apply the rule.\
For this, there are three main APIs that are of significance:

1. POST /api/v1/data/upload/
2. POST /api/v1/rule/
3. GET /api/v1/tool/calculate-risk-index/{rule_id}

The first one is used to upload a dataset to the service.\
The second one is used to define a rule.\
The third one is used to apply the rule to the dataset, and to fetch the results.\

For more examples, please view the swagger documentation.

# Contribution
Please contact the maintainer of this repository.

# License
[European Union Public License 1.2](https://github.com/openagri-eu/pest-and-disease-management/blob/main/LICENSE)
