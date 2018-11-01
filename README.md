# Twitter Tools

*An assortment of Python scripts to manipulate Twitter JSON data for data analytics*

Hello and welcome to my Swiss-army knife for manipulating Twitter data. Written hurriedly over the course of a summer, much of the code is messy and undergoing development for readability and improvement. The tools within are specifically designed to produce a geospatial-sentiment analysis of Tweets. 

Please feel free to explore or leave comment!

## Dependencies

- [**Python 3**](https://www.python.org/downloads/)
- [**Afinn**](https://github.com/fnielsen/afinn)
Afinn is the primary sentiment engine used within the code. Please install it by navigating to their Github page which includes more information about the project.
- [**Carmen**](https://github.com/mdredze/carmen-python/)
Carmen is a tool developed by researchers at Johns Hopkins University to determine the location of Tweets. The engine has been released in Python and Java.
- [**Joblib**](https://github.com/joblib/joblib)
Joblib is a tool used to enable multi-threading support for Python. It's been used in the project to speed up long tweet operations.


## Configuration

Please note that these tools assume that you have a directory (or directory hierarchy) that contain files which have tweets in JSON format. 

This code has been tested using tweets retrieved and stored by Apache Flume.

## Tools

### Tweets Module 

The Tweets module contains code to quickly fetch tweets or fields from tweets. It serves as a layer of abstraction to get a list of tweets for further processing. 

The module also includes utility functions to save data for later processing or for loading saved data.

### Geo Module

The Geo module contains code for location-tagging and location-processing of tweets. Within it, I have included constants of countries and states within the United States to assist in later analysis.

Code within the module will find a distribution of sentiment across countries, states within the United States, or cities. In addition, the code assists in tagging tweets with coordinate data, and comparing geo-spatial data.

### Sent Module

The Sent module contains code to find the sentiment expressed in a list of tweets and save that sentiment for later processing.


## To-Do

- [ ] Clean up location code
	- [x] Consolidate location code
	- [ ] Review location-tagging and location-processing code in geo.py
	- [ ] Clarify code with comments
- [ ] Clean up user matrix analysis code
	- [ ] Consolidate user matrix analysis code
	- [ ] Review user matrix code
	- [ ] Clarify code with comments
- [ ] Clean up sentiment code
	- [ ] Consolidate sentiment code
	- [ ] Review code
	- [ ] Clarify code with comments
- [ ] Test code with tweets retrieved from non-Flume streaming services
- [x] Create a config template
- [x] Finish READMe
