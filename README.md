[![License](https://img.shields.io/badge/License-Apache2-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0) [![Community](https://img.shields.io/badge/Join-Community-blue.svg)](https://callforcode.org/slack) [![Hacktoberfest](https://img.shields.io/badge/Celebrate-Hacktoberfest-orange.svg)](https://call-for-code-for-racial-justice.github.io/Hacktoberfest/#/?id=main)

# TakeTwo Solution Starter - WebAPI Backend

The TakeTwo Web API is used to take facilitate the centralization of data, such as that gathered through the [TakeTwo Chrome extension](https://github.com/Call-for-Code-for-Racial-Justice/taketwo-marker-chromeextension) and populate a backend database. This data can then be used to train a model to predict racially biased language. The TakeTwo API also allows a content creator to scan their writing for potentially racially biased language. 

The API is built on open source technologies like [Python](https://www.python.org/), [FastAPI](https://fastapi.tiangolo.com/), [Swagger](https://swagger.io/) and [OAuth](https://oauth.net/) and can be deployed on open source container platform like [Kubernetes](https://kubernetes.io/).

The racially biased terms are loaded into a backend database. The code is set up to run the API locally with a [CouchDB](https://couchdb.apache.org/) backend database or [IBM Cloudant](https://www.ibm.com/uk-en/cloud/cloudant) database.

To run with CouchDB, you will need to deploy a CouchDB Docker image either locally or on a Kubernetes cluster.

There is a front-end HTML page that serves as an example text editor.

</br>

### Description of TakeTwo API

This API is part of the Call for Code for Racial Justice TakeTwo project. This API is used to capture the data crowdsourced by our contributors through the [TakeTwo Chrome extension tool](https://github.com/Call-for-Code-for-Racial-Justice/taketwo-marker-chromeextension/blob/main/README.md).

The API is used to fetch the defined categories of racial bias and serve them in the extension tool. It also captures the data highlighted by contributors and posts it to a backend database. This data is used to train an [ML model](https://github.com/Call-for-Code-for-Racial-Justice/taketwo-datascience/blob/main/README.md) that can detect racial bias.

## Datasets

The database contains the following fields:

- ``"_id"``: *Database field* (optional)
- ``"_rev"``: *Database field*
- ``"user_id"``: *The user ID*
- ``"flagged_string"``: *The word or phrase that has been highlighted by the user.*
- ``"category"``: *The category that has been selected for the type of racial bias present in the highlighted word or phrase.*
- ``"info"``: *Additional information; context description provided by the user.* (optional)
- ``"url"``: *The url from where the word or phrase was highlighted.*


</br>

This project has defined a number of categories of racial bias, which are used by a text classification model (outlined below). We welcome feedback on these:

- Appropriation
- Stereotyping
- Under-Representation
- Gaslighting
- Racial Slur
- Othering

Definitions of these categories can be found on the TakeTwo [webpage](https://github.com/Call-for-Code-for-Racial-Justice/TakeTwo/blob/main/README.md).

</br>

## Learning objectives

In this tutorial, you will learn how to:
- Clone the TakeTwo repositories.
- Install the Python prerequisites.
- Start a CouchDB container.
- Launch the application.
- Deploy to Kubernetes (optionally).
- Use the API.

## Prerequisites

To complete the steps in this tutorial you need:
- Install Python3
- Install Python3 dev kit
- Install gcc (c compiler)
- Install wheel
- Install Docker

## Estimated time

Completing this tutorial should take about 15 minutes.

## Getting started

#### Clone the TakeTwo repository

To run this API locally you will need to clone this repo. 
If you plan on making contributions to the project, make sure to fork the repo and clone your fork instead (see CONTRIBUTING.md for more info):

```git clone https://github.com/Call-for-Code-for-Racial-Justice/taketwo-webapi.git```

#### Install the Python prerequisites

Run the following command to create a virtual environment:

```python3 -m venv env```

Activate virtual environment:

```source env/bin/activate```

Install the packages needed from the requirements.txt file:

```pip install -r requirements.txt```

Navigate to the folder which contains the API code:

```cd taketwo-webapi```

#### Start a CouchDB container

Before launching the application, set the name of your CouchDB database:

```export DBNAME=taketwodatabase```

To run the API with a CouchDB backend, start a couchDB container before running the main.py code:

```docker run -p 5984:5984 -d -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=password couchdb```

The Couch DB web interface will be available at http://localhost:5984. 

#### Configure your IBM App Id
- See the following video for how to set it up https://www.loom.com/share/937c89f086aa420597cc55b97a987031

#### Configure the application
Copy `.env.sample` file to `.env` file in the same directory. Fill out the CouchDB database and IBM App Id service credentials.

```
#CouchDB Credentials
DB_HOST=
DB_PORT=
DB_NAME=
DB_USERNAME=
DB_PASSWORD=

#IBM AppID Credentials
CLIENT_ID=
SECRET=
OAUTH_SERVER_URL=
```
- DB_HOST: localhost if running locally
- DB_PORT, DB_USERNAME, DB_PASSWORD: use what you provided in the "docker run -p 5984:5984 -d -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=password couchdb" step
- DBNAME: taketwodatabase

#### Launch the application

Run the Python api code:

```uvicorn main:app --reload```

</br>

### Deploy to Kubernetes

You can build your own using the Dockerfile in this repo. To build a new image, run the following command in a terminal window:

```docker build -t <dockerusername>/taketwo_api .```

To push the image to Docker Hub, run the following:

```docker login```
```docker push <dockerusername>/taketwo_api```

</br>

### Use the API

When the API is running, the main url will show an example text editor, which can be used to make requests to the backend data. You can type in the text box and then press check. Text that could be racially biased will be highlighted as shown in the following example.

Open a browser to [http://localhost:8000](http://localhost:8000)

</br>

![](docs/assets/take-two-text-editor.png)

With the API running, you can also install the TakeTwo Chrome extension and this will enable data capture via a browser. 

### Review the TakeTwo OpenAPI documentation

For an overview of the available endpoints navigate to [http://localhost:8000/docs](http://localhost:8000/docs)

![TakeTwo Swagger Doc](docs/assets/api-swaggerdoc.png)

### Contributing

We welcome contributions! For details on how to contributing please read the [CONTRIBUTING](CONTRIBUTING.md) file in this repo.

This project is still very much a work in progress, however our hope for the future is that this is a step towards a more informed media culture that is more aware of racial bias in media content. We hope this can be built out so that it can be used in a range of areas; news, social media, forums, code etc.

We also hope to expand the project to enable detection of racial bias in audio and video in the future.

We hope you will help us in this open source community effort!

## Summary

Once the TakeTwo database and Python service is running, the TakeTwo endpoints can be called to get, save, delete, update data in the database. New text can be analyzed for potentially racially biased terminology.

## Related Links

There are a number of other components related to this project:

- [TakeTwo Data Science](https://github.com/Call-for-Code-for-Racial-Justice/taketwo-datascience/blob/main/README.md) - Contains data science work for building and training the model.
- [TakeTwo Marker Chrome Extension](https://github.com/Call-for-Code-for-Racial-Justice/taketwo-marker-chromeextension/blob/main/README.md) - Code for the Chrome extension used to crowdsource data for training the ML model.

## License

This solution starter is made available under the [Apache 2 License](LICENSE).
