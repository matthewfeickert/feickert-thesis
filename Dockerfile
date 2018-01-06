# Following heavily from https://hub.docker.com/r/fermiumlabs/latex-docker/~/dockerfile/
FROM ubuntu:xenial

MAINTAINER Matthew Feickert <matthew.feickert@cern.ch>

ENV HOME /root
WORKDIR /root

ENV DEBIAN_FRONTEND noninteractive

# Install general dependencies
RUN apt-get -qq -y update
RUN apt-get -qq -y install curl wget build-essential zip python-pip jq git libfontconfig \
    locales software-properties-common sshpass

# Install latest TeXLive
RUN wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
RUN tar -zxvf install-tl-unx.tar.gz
RUN wget https://raw.githubusercontent.com/fermiumlabs/latex-docker/master/texlive.profile
RUN install-*/install-tl --profile=texlive.profile
RUN rm -rf install-tl*

# Export useful TeX Live paths
ENV PATH /opt/texbin:$PATH
ENV PATH /usr/local/texlive/2017/bin/x86_64-linux:$PATH

# Test LaTeX
RUN wget ftp://www.ctan.org/tex-archive/macros/latex/base/small2e.tex
RUN latex small2e.tex
RUN xelatex small2e.tex

RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /root/*

WORKDIR /root
VOLUME ["/root"]
