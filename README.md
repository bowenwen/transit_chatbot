# Transit Chatbot
A friendly trip planning chatbot that provides transit directions from A to B and information on the next bus arrival time.

Developed using the open-source conversational AI library [Rasa stack](https://rasa.com/). The framework is generic, however, the implementation is specific to transit services in Metro Vancouver, BC, Canada offerred by TransLink.

The chatbot is not an official TransLink product.


## Getting started: test chatbot in Jupyter with docker

### Get a copy on your local

`git clone https://github.com/moh-salah/transit_chatbot.git`

### Start container

`docker-compose up`

*You can access the Jupyter Notebook working environment on: `http://localhost:8888/`.*

*You can check the status of the rasa action server on: `http://localhost:5055/`.*

*You can test the pre-trained chatbot in the terminal within the docker container environment: `python -m rasa_core.run -d models/dialogue -u models/nlu/default/current --endpoints endpoints.yml --debug`*

### Cleanup containers

`docker-compose down`


## Deploying the chatbot with docker

Deploying trained chatbot is easy with rasa prebuilt images

### Get a copy on your local

`git clone https://github.com/moh-salah/transit_chatbot.git`

`cd rasa_docker`

### Retrain the model with Rasa Docker (Optional)

#### Train rasa core

`
docker run -v $pwd/:/app/project -v $pwd/models/rasa_core:/app/models rasa/rasa_core:0.12.3 train --domain project/domain.yml --stories project/data/stories.md --config project/policy_config.yml --out models
`

#### Train rasa nlu

`
docker run -v $pwd/:/app/project -v $pwd/models/rasa_nlu:/app/models rasa/rasa_nlu:0.13.8-spacy run python -m rasa_nlu.train -c project/config.yml -d project/data/data.json -o models --project current
`

### Build a custome Rasa action image (Optional)

`
docker build --tag my_action_image .
`

*If you decide to build your own image, please modify the docker-compose file accordingly.*

### Start chatbot services

`
docker-compose up -d
`

*You need to set up your own chatbot platform connectors with relevant credentials, read more about connectors [here](https://rasa.com/docs/core/0.13.2/connectors/).*

*While you are configuring your connectors, you might want to use a tunnel service if you are not configuring on a server or cloud service with public domain. [ngnork](https://dashboard.ngrok.com/get-started) offers free tunnel service.*


### Cleanup containers

`docker-compose down`


*For more information on working with Rasa Docker Images, [check out their guide](https://rasa.com/docs/core/docker_walkthrough/).*


