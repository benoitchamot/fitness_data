# fitness_data
Portfolio project based on Fitbit Data. Suggested in Google Data Analytics Professional Certificate.

## Data source
The data used in this project and contained in the CSV files in `/Data` come from https://www.kaggle.com/datasets/arashnic/fitbit. The data are published under the [CC0: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/) license. All the other files, code and notes are my own.

## File structure
- `Data` is a directory that contains the data in CSV files
- `Server` is a directory containing the database (`fitness_db.sqlite`) and the notebook used to populate them. The directory also contains the code running the Flask server.
- `Dashboard` contains the HTML, CSS and JavaScript files to retrieve the data from the API and Flask app in `Server`.
- `data_exploration.ipynb` is a Jupyter notebook used for the preliminary data exploration, analysis and visualisation. 
