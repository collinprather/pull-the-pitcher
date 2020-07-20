FROM manifoldai/orbyter-ml-dev:2.0

# ubuntu installing - graphviz, nano, libpq (for psycopg2)
RUN apt-get update &&\
    apt-get install graphviz -y &&\
    apt-get install nano -y &&\
    apt-get install libpq-dev -y

# exposing default port for streamlit
EXPOSE 8501

# making directory of app
WORKDIR /pull-the-pitcher

# copy over requirements
COPY requirements.txt ./requirements.txt

# installing required packages
RUN pip install -r requirements.txt --no-cache-dir

# copying all app files to image
COPY . .

# cmd to launch app when container is run
CMD streamlit run webapp/app.py

# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'

# RUN bash -c 'echo -e "\
# [server]\n\
# enableCORS = false\n\
# " > /root/.streamlit/config.toml'
