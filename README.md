# Transit Chatbot
A friendly trip planning chatbot that provides transit directions from A to B and information on the next bus arrival time.

Developed using the open-source conversational AI library [Rasa stack](https://rasa.com/). The framework is generic, however, the implementation is specific to transit services in Metro Vancouver, BC, Canada offerred by TransLink.

The chatbot is not an official TransLink product.

## Model Training and Testing

A customized docker image is available for model training and testing

`git clone https://github.com/moh-salah/transit_chatbot.git`

- Use prebuilt image `bowenwen/rasa_chatbot_nb:latest` and start container using docker-compose, 
`docker docker-compose up -d`

- Optionally, you can build the docker image yourself, and run it
`docker build -t "transit_chatbot" .`
`docker run -p 8888:8888 -v /:/home/jovyan/transit_chatbot transit_chatbot`


## Model Deployment

More to come...