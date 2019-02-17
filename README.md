# Transit Chatbot
A friendly trip planning chatbot that provides transit directions from A to B and information on the next bus arrival time.

Developed using the open-source conversational AI library [Rasa stack](https://rasa.com/). The framework is generic, however, the implementation is specific to transit services in Metro Vancouver, BC, Canada offerred by TransLink.

The chatbot is not an official TransLink product.


## Getting started: testing in Jupyter with docker

### Get a copy on your local

`git clone https://github.com/moh-salah/transit_chatbot.git`

### Use prebuilt image to start container using docker-compose

`docker-compose up`

*You can access the Jupyter Notebook working environment on: `http://localhost:8888/`.*

*You can check the status of the rasa action server on: `http://localhost:5055/`.*

### To cleanup the docker containers

`docker-compose down`


## Deploying the chatbot with docker

Deploying trained chatbot is easy with rasa prebuilt images

### Get a copy on your local

`git clone https://github.com/moh-salah/transit_chatbot.git`
`cd rasa_docker`

### Retrain the model with Rasa Docker (Optional)

#### Train rasa core

`
docker run -v $pwd/:/app/project -v $pwd/models/rasa_core:/app/models rasa/rasa_core:0.12.3 train --domain project/domain.yml --stories project/data/stories.md --out models
`

#### Train rasa nlu

`
docker run -v $pwd/:/app/project -v $pwd/models/rasa_nlu:/app/models rasa/rasa_nlu:0.13.8-spacy run python -m rasa_nlu.train -c config.yml -d project/data/data.json -o models --project current
`

### Build a custome Rasa action image (Optional)

`
docker build --tag my_action_image .
`

*If you decide to build your own, please modify the docker-compose file accordingly.*

### start chatbot service

`
docker-compose up -d
`

*You need to set up your own chatbot services and configure connectors, read more about connectors [here](https://rasa.com/docs/core/0.13.2/connectors/).*

### To cleanup the docker containers

`docker-compose down`


*For more information on working with Rasa Docker Images, [check out their guide](https://rasa.com/docs/core/docker_walkthrough/).*


