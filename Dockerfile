FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y build-essential && apt-get install -yq --no-install-recommends \
    libtiff-dev \
    python-numpy \
    python-dev \
    python-opengl

WORKDIR /app

COPY src src
COPY setup.py setup.py

ENV PYTHONPATH=/app/src:${PYTHONPATH}

RUN conda install -y pyopengl
RUN conda install -y libtiff

RUN pip install -e .
RUN pip install numpy
RUN pip install libtiff

ENTRYPOINT ["python", "/app/src/tools/convert_subtree.py"]
