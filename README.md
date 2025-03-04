# sqlalchemy-challenge

This repository contains all work and solutions for the sqlalchemy challenge. `climate_starter.ipynb` contains all intial analysis, and `app.py` contains the API. 

## Analysis

After setting up sqlalchemy to reflect the existing database, the most recent date was found and a year prior to that was deduced. Using this year of data, a plot for precipitation was generated. Along with this, summary statistics of this year of data exist in the output of block `11` of `climate_Starter.ipynb`. The station observations were counted to decide which station had the most observations, which ended up being station `USC00519281`. Then, the previous 12 months of temperature data was collected. The graph for this can be seen in block the output of `15` of `climate_Starter.ipynb`. 

## API

After the initial analysis, I moved on to creating the API. The API has the following routes:
- /api/v1.0/precipitation
    - 12 Months of precipitaton data
- "/api/v1.0/stations
    - Info on all stations
- "/api/v1.0/tobs
    - Temperature info
- "/api/v1.0/\<start>
    - (please use yyyy-mm-dd format)  
- "/api/v1.0/\<start>/\<end>
    - (please use yyyy-mm-dd format)
 
Each route returns a json object with data explained above. 
