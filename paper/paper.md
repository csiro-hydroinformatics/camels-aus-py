---
title: "camels_aus: A Python package to access hydrometeorological time series and landscape attributes of catchments in Australia"
tags:
    - Hydrology
    - Hydrological data
    - CAMELS
    - Python
authors:
    - name: Jean-Michel Perraud
      orcid: 0000-0003-2305-8961
      affiliation: "1"
affiliations:
    - name: Commonwealth Scientific and Industrial Research Organisation, Canberra, Australia
      index: 1
date: 27 February 2022
bibliography: paper.bib
---

# Summary

**camels_aus** helps Python users read and exploit the CAMELS-AUS hydrometeorological dataset [@Fowler2021]. CAMELS-AUS is the Australian edition of the Catchment Attributes and Meteorology for Large-sample Studies (CAMELS) series of datasets, which are increasingly used for many large scale hydrological modelling studies, in particular in our contemporary context where novel machine learning techniques require large amounts of data. CAMELS-AUS and its siblings are instances adhering to the FAIR data principles (findable, accessible, interoperable and reusable) [@Wilkinson2016] in the field of Hydrology.

The **camels_aus** Python package is a facade that takes care of the low level data ingestion from CAMELS-AUS text files into an in-memory format using [xarray](http://xarray.pydata.org/en/stable/index.html). It is hiding the on-disk representation of CAMELS-AUS while preservering the integrity of the source data.

designed to minise the amount of code required by users.

# Statement of Need

Ingestion of data from their on-disk representation is a necessary but tedious, time consuming and error-prone aspect of data science. The CAMELS-AUS data consists mostly of comma-separated values (CSV) files in a codified directory structure. CSV files may be an entry level solution from a technical point of view, but pragmatically they are a sound choice, highly accessible and interoperable. There is however a gap between the on-disk representation and the modelling environment of the user. This situation fosters the implementation of numerous _ad hoc_, inefficient and idiosyncratic data ingestion systems, often limited in use to one person only.

The **camels_aus** package aims to fill this gap and bring the CAMELS-AUS data to Python users with minimal friction. It should be noted that CAMELS datasets are siblings, and a unified Python package facilitating access to all CAMELS datasets would benefit large-scale hydrological studies. However, differences in the data format makes this a non-trivial design and implementation endeavour, and **camels_aus** is deliberately limited in scope to the Australian edition.

# State of the Field

To our knowledge there is no prior published Python software similar to **camels_aus**, notwithstanding 
Various endeavours to have higher level packages to access the CAMELS-US dataset. 

[hydroDL](https://github.com/mhpi/hydroDL)

Kratzert.

SWIFT format relationships

Currently, there are a few open-source Python packages that can perform depression filling on digital elevation data, such as RichDEM [@Barnes2018] and [whitebox](https://github.com/giswqs/whitebox-python), the Python frontend for [WhiteboxTools](https://github.com/jblindsay/whitebox-tools) [@Lindsay2018]. However, there are no Python packages offering tools for delineating the nested hierarchy of surface depressions and catchments as well as simulating inundation dynamics. The **camels_aus**  Python package is intended for filling this gap.

# camels_aus Functionality

The key functionality of the **camels_aus** package is organized into several modules:

- [filtering](https://github.com/giswqs/camels_aus/blob/master/camels_aus/filtering.py): Smoothing DEMs using mean, median, and Gaussian filters.
- [filling](https://github.com/giswqs/camels_aus/blob/master/camels_aus/filling.py): Delineating surface depressions from DEMs using the traditional depression filling method.
- [slicing](https://github.com/giswqs/camels_aus/blob/master/camels_aus/slicing.py): Delineating the nested hierarchy of surface depressions using the level-set method; computing topological and geometric properties of depressions; and exporting depression properties as a CSV file.
- [mounts](https://github.com/giswqs/camels_aus/blob/master/camels_aus/mounts.py): Delineating the nested hierarchy of elevated features (i.e., mounts) using the level-set method; computing topological and geometric properties of mounts; and exporting mount properties as a CSV file.
- [toolbox](https://github.com/giswqs/camels_aus/blob/master/camels_aus/toolbox): An [ArcGIS](https://www.esri.com/en-us/arcgis/about-arcgis/overview) toolbox for delineating the nested hierarchy of surface depressions and simulating inundation dynamics.

# camels_aus Tutorials

The **camels_aus** Python package has a C library dependency called [GDAL](https://gdal.org/index.html), which can be challenging for some users to install on their computer. Alternatively, users can try out the **camels_aus** package using just a browser without having to install anything on their computer.

- Try it out with Binder: <https://gishub.org/camels_aus-binder>
- Try it out with Google Colab: <https://gishub.org/camels_aus-colab>
- Help documentation: <https://camels_aus.gishub.org>

The **camels_aus** package also provides an ArcGIS toolbox for delineating the nested hierarchy of surface depressions and catchments as well as simulating inundation dynamics. Video tutorials for using the toolbox are available at <https://camels_aus.gishub.org/get-started/#arcgis-toolbox>.

![The ArcGIS toolbox for the camels_aus Python package](https://raw.githubusercontent.com/giswqs/camels_aus/master/images/toolbox_0.png)

# Acknowledgments

The author would like to thank the open-source community, especially the developers of numpy [@Harris2020], scipy [@Virtanen2020], scikit-image [@Van_der_Walt2014], matplotlib [@Hunter2007], and richDEM [@Barnes2018]. These open-source packages empower the **camels_aus** Python package.

# References
