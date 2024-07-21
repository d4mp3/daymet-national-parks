FROM python:3.10-bookworm
LABEL maintainer="dampe"

ENV DEBIAN_FRONTEND=noninteractive

ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=/etc/hadoop
ENV USER=root
ENV PATH=${HADOOP_HOME}/bin/:$PATH

RUN apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq --no-install-recommends \
    apt-utils \
    curl \
    wget \
    netcat-traditional && \
    apt-get autoremove -yqq --purge

# ENV TZ="Europe/Warsaw"

# RUN apt-get install -yqq openjdk-8-jdk

RUN wget http://www.mirbsd.org/~tg/Debs/sources.txt/wtf-bookworm.sources
RUN mkdir -p /etc/apt/sources.list.d
RUN mv wtf-bookworm.sources /etc/apt/sources.list.d/
RUN apt-get update
RUN apt-get install -yqq openjdk-8-jdk
 
# Setup JAVA_HOME 
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
RUN export JAVA_HOME

RUN mkdir -p /opt/hadoop

RUN wget -c -O hadoop.tar.gz https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar xvf hadoop.tar.gz --directory=/opt/hadoop --exclude=hadoop-${HADOOP_VERSION}/share/doc --strip 1 && \
    rm -rf hadoop.tar.gz && \
    ln -s /opt/hadoop/etc/hadoop /etc/hadoop && \
    mkdir /opt/hadoop/logs && \
    mkdir /hadoop-data

COPY ./conf ./conf

RUN mv ./conf/* /etc/hadoop/ && \
    rm -rf ./conf

COPY ./entrypoint.sh .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
