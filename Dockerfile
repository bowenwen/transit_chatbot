# use jupyter/tensorflow-notebook: as base
# Credits: 
# https://github.com/jupyter/docker-stacks/
# https://hub.docker.com/r/jupyter/tensorflow-notebook/tags

ARG BASE_CONTAINER=jupyter/tensorflow-notebook:0f73f7488fa0
FROM $BASE_CONTAINER

LABEL maintainer="Bo Wen"

USER $NB_UID

# Upgrade pip
RUN pip install --upgrade pip

# Install additional python packages
RUN pip install --user \
    rasa_core==0.12.3 \
    rasa_nlu==0.13.8 \
	sklearn-crfsuite==0.3.6 \
    spacy==2.0.18

# Install spacey models
RUN python -m spacy download en && \
	python -m spacy download en_core_web_sm
	
# Install nbmultitask for multithreading in Notebook
RUN pip install --user nbmultitask==0.1.0
	
USER root
	
# Set timezone
ENV TZ=America/Vancouver
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR $HOME/work

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start-notebook.sh"]

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID