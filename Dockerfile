FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y build-essential && apt-get install -y \
    python3-numpy \
    python3-dev \
    python3-opengl \
    git


WORKDIR /app

COPY src src
COPY setup.py setup.py

RUN /opt/conda/bin/activate

ENV PYTHONPATH=/app/src:${PYTHONPATH}

RUN pip install numpy
RUN conda install -y libtiff=4.0.10
RUN pip install -e .

RUN conda install -y pyopengl

WORKDIR /tmplibtiff
RUN git clone https://github.com/pearu/pylibtiff.git .
RUN pip install -e .

ENTRYPOINT ["/opt/conda/bin/python", "/app/src/tools/convert_subtree.py"]
