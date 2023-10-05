Apptainer Example Definition Files
==================================

.. contents:: Table of Contents
    :depth: 2


bilby.def
---------

::

    BootStrap: docker
    From: mambaorg/micromamba:1.4.6-jammy

    %post
        micromamba install -qy -n base -c conda-forge python=3.10 bilby gwpy python-lalsimulation


astrometry.net.def
------------------

::

    BootStrap: docker
    From: debian:12-slim

    %post
        apt-get update -y
        apt-get install -y build-essential wget libcairo2-dev libnetpbm-dev netpbm \
                            libpng-dev libjpeg-dev python-dev-is-python3 python3-numpy \
                            python3-astropy python3-dev zlib1g-dev \
                            libbz2-dev swig libcfitsio-dev
        apt-get clean all -y
        cd /opt
        wget https://github.com/dstndstn/astrometry.net/releases/download/0.94/astrometry.net-0.94.tar.gz
        tar xvzf astrometry.net-0.94.tar.gz
        rm astrometry.net-0.94.tar.gz
        cd astrometry.net-0.94
        make
        make py
        make extra
        make install
        rm -rf /opt/astrometry.net-0.94

    %runscript
        export PATH=$PATH:/usr/local/astrometry/bin
        exec "$@"


hotpants.def
------------

::

    BootStrap: docker
    From: debian:12-slim

    %post
        apt-get update -y
        apt-get install -y build-essential git libcfitsio-dev
        apt-get clean all -y
        cd /opt && git clone https://github.com/acbecker/hotpants.git && cd hotpants
        make COPTS="-funroll-loops -fcommon -O3 -ansi -std=c99 -pedantic-errors -Wall -D_GNU_SOURCE" libs="-lm -lcfitsio"
        install -t /usr/local/bin hotpants extractkern maskim
        rm -rf /opt/hotpants


psfex.def
----------------

::

    BootStrap: docker
    From: debian:12-slim

    %post
        apt-get update -y
        apt-get install -y psfex
        apt-get clean all -y

    %runscript
        psfex $@


swarp.def
----------------

::

    BootStrap: docker
    From: debian:12-slim

    %post
        apt-get update -y
        apt-get install -y swarp
        apt-get clean all -y

    %runscript
        SWarp $@


heasoft.def
-----------

::

    BootStrap: docker
    From: ubuntu:22.04

    %files
        /apps/sources/h/heasoft/heasoft-6.32.1src.tar.gz /

    %labels
        version "6.32.1"
        description "HEASoft 6.32.1 https://heasarc.gsfc.nasa.gov/lheasoft/"
        maintainer "NASA/GSFC/HEASARC https://heasarc.gsfc.nasa.gov/cgi-bin/ftoolshelp"

    %environment
        export DEBIAN_FRONTEND=noninteractive

    %post
        apt-get update
        apt-get -y upgrade
        apt-get -y install gcc \
        gfortran \
        g++ \
        libcurl4 \
        libcurl4-gnutls-dev \
        libncurses5-dev \
        libreadline6-dev \
        make \
        ncurses-dev \
        perl-modules \
        python3-dev \
        python3-pip \
        python3-setuptools \
        python-is-python3 \
        tcsh \
        wget \
        xorg-dev
        apt-get clean
        rm -rf /var/lib/apt/lists/*
        mkdir -p /opt/heasoft/caldb

        tar xzf heasoft-6.32.1src.tar.gz
        rm heasoft-6.32.1src.tar.gz
        pip3 install --only-binary=:all: astropy numpy scipy matplotlib
        cd /heasoft-6.32.1/BUILD_DIR/
        ./configure --prefix=/opt/heasoft 2>&1 | tee /configure.log
        make 2>&1 | tee /build.log
        make install 2>&1 | tee /install.log
        make clean 2>&1
        /bin/bash -c 'cd /opt/heasoft/; for loop in x86_64*/*; do ln -sf $loop; done'
        cd /heasoft-6.32.1
        cp -p Xspec/BUILD_DIR/hmakerc /opt/heasoft/bin/
        cp -p Xspec/BUILD_DIR/Makefile-std /opt/heasoft/bin/
        rm -rf Xspec/src/spectral
        cd
        gzip -9 /*.log
        cp -p /heasoft-6.32.1/Release_Notes* /opt/heasoft/

        cd /opt/heasoft/caldb \
        && wget https://heasarc.gsfc.nasa.gov/FTP/caldb/software/tools/caldb.config \
        && wget https://heasarc.gsfc.nasa.gov/FTP/caldb/software/tools/alias_config.fits

        echo "export CC=/usr/bin/gcc" >> $APPTAINER_ENVIRONMENT
        echo "export CXX=/usr/bin/g++" >> $APPTAINER_ENVIRONMENT
        echo "export FC=/usr/bin/gfortran" >> $APPTAINER_ENVIRONMENT
        echo "export PERL=/usr/bin/perl" >> $APPTAINER_ENVIRONMENT
        echo "export PERLLIB=/opt/heasoft/lib/perl" >> $APPTAINER_ENVIRONMENT
        echo "export PERL5LIB=/opt/heasoft/lib/perl" >> $APPTAINER_ENVIRONMENT
        echo "export PYTHON=/usr/bin/python" >> $APPTAINER_ENVIRONMENT
        echo "export PYTHONPATH=/opt/heasoft/lib/python:/opt/heasoft/lib" >> $APPTAINER_ENVIRONMENT
        echo "export PATH=/opt/heasoft/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" >> $APPTAINER_ENVIRONMENT
        echo "export HEADAS=/opt/heasoft" >> $APPTAINER_ENVIRONMENT
        echo "export LHEASOFT=/opt/heasoft" >> $APPTAINER_ENVIRONMENT
        echo "export FTOOLS=/opt/heasoft" >> $APPTAINER_ENVIRONMENT
        echo "export LD_LIBRARY_PATH=/opt/heasoft/lib" >> $APPTAINER_ENVIRONMENT
        echo "export LHEAPERL=/usr/bin/perl" >> $APPTAINER_ENVIRONMENT
        echo "export PFCLOBBER=1" >> $APPTAINER_ENVIRONMENT
        echo "export PFILES=/heasoft/pfiles;/opt/heasoft/syspfiles" >> $APPTAINER_ENVIRONMENT
        echo "export FTOOLSINPUT=stdin" >> $APPTAINER_ENVIRONMENT
        echo "export FTOOLSOUTPUT=stdout" >> $APPTAINER_ENVIRONMENT
        echo "export LHEA_DATA=/opt/heasoft/refdata" >> $APPTAINER_ENVIRONMENT
        echo "export LHEA_HELP=/opt/heasoft/help" >> $APPTAINER_ENVIRONMENT
        echo "export EXT=lnx" >> $APPTAINER_ENVIRONMENT
        echo "export PGPLOT_FONT=/opt/heasoft/lib/grfont.dat" >> $APPTAINER_ENVIRONMENT
        echo "export PGPLOT_RGB=/opt/heasoft/lib/rgb.txt" >> $APPTAINER_ENVIRONMENT
        echo "export PGPLOT_DIR=/opt/heasoft/lib" >> $APPTAINER_ENVIRONMENT
        echo "export POW_LIBRARY=/opt/heasoft/lib/pow" >> $APPTAINER_ENVIRONMENT
        echo "export XRDEFAULTS=/opt/heasoft/xrdefaults" >> $APPTAINER_ENVIRONMENT
        echo "export TCLRL_LIBDIR=/opt/heasoft/lib" >> $APPTAINER_ENVIRONMENT
        echo "export XANADU=/opt/heasoft" >> $APPTAINER_ENVIRONMENT
        echo "export XANBIN=/opt/heasoft" >> $APPTAINER_ENVIRONMENT
        echo "export CALDB=https://heasarc.gsfc.nasa.gov/FTP/caldb" >> $APPTAINER_ENVIRONMENT
        echo "export CALDBCONFIG=/opt/heasoft/caldb/caldb.config" >> $APPTAINER_ENVIRONMENT
        echo "export CALDBALIAS=/opt/heasoft/caldb/alias_config.fits" >> $APPTAINER_ENVIRONMENT

    %runscript
        . /opt/heasoft/headas-init.sh
        exec "$@"


sextractor.def
---------------------

::

    BootStrap: docker
    From: debian:12-slim

    %post
        apt-get update -y
        apt-get install -y sextractor
        apt-get clean all -y

    %runscript
        source-extractor $@


iraf-2.16_i686.def
------------------

::

    BootStrap: docker
    From: almalinux:9

    %files
        /apps/sources/i/iraf/2.16-i686_skylake.tar.gz iraf-2.16-i686.tar.gz

    %post
        yum update -y
        yum install -y xterm csh gcc make flex libXmu-devel libX11-devel glibc.i686 zlib-devel.i686 libcurl-devel.i686 expat-devel.i686 readline-devel.i686
        yum clean all
        mkdir -p /usr/local/i686/gnu && tar -xvzf iraf-2.16-i686.tar.gz -C /usr/local/i686/gnu/ && rm iraf-2.16-i686.tar.gz
        cd /usr/local/i686/gnu && mv 2.16-i686 iraf-2.16
        cd /usr/lib && ln -svf libreadline.so libreadline.so.6

    %runscript
        source /usr/local/i686/gnu/iraf-2.16/environ.sh
        export stsdasbc=/usr/local/i686/gnu/iraf-2.16/stsdasbc
        if [ -z $@ ]; then
            exec cl
        else
            exec "$@"
        fi
