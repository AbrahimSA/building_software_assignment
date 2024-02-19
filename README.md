# Building Robust Software Summative Assignment
By the end of this course, you will build an installable Python package that analyzes data retrieved from the GitHub API (or another web data provider of your choice). You'll work in teams and collaborate using tools on GitHub.


## Package API specifications
#### `class yourteamrepo.Analysis.Analysis(analysis_config:str)`
```
''' Load config into an Analysis object

Load system-wide configuration from `configs/system_config.yml`, user configuration from
`configs/user_config.yml`, and the specified analysis configuration file

Parameters
----------
analysis_config : str
    Path to the analysis/job-specific configuration file

Returns
-------
analysis_obj : Analysis
    Analysis object containing consolidated parameters from the configuration files

Notes
-----
The configuration files should include parameters for:
    * GitHub API token
    * ntfy.sh topic
    * Plot color
    * Plot title
    * Plot x and y axis titles
    * Figure size
    * Default save path

'''
```

##### `load_data()`
```
''' Retrieve data from the GitHub API

This function makes an HTTPS request to the GitHub API and retrieves your selected data. The data is
stored in the Analysis object.

Parameters
----------
None

Returns
-------
None

'''
```

##### `compute_analysis() -> Any`
```
'''Analyze previously-loaded data.

This function runs an analytical measure of your choice (mean, median, linear regression, etc...)
and returns the data in a format of your choice.

Parameters
----------
None

Returns
-------
analysis_output : Any

'''
```

##### `notify_done(message: str) -> None`
```
''' Notify the user that analysis is complete.

Send a notification to the user through the ntfy.sh webpush service.

Parameters
----------
message : str
  Text of the notification to send

Returns
-------
None

'''
```

##### `plot_data(save_path:Optional[str] = None) -> matplotlib.Figure`
* *Optional* if your team only has 3 members
```
''' Analyze and plot data

Generates a plot, display it to screen, and save it to the path in the parameter `save_path`, or 
the path from the configuration file if not specified.

Parameters
----------
save_path : str, optional
    Save path for the generated figure

Returns
-------
fig : matplotlib.Figure

'''
```


## Usage example
execute this to install the package.
``` python
!pip install git+https://github.com/abrahimsa/building_software_assignment
from building_software_assignment import Analysis

# Load config into an Analysis object
analysis_obj = Analysis('config.yml')

# Retrieve data from the GitHub API
analysis_obj.load_data()

# Analyze previously-loaded data.
analysis_output = analysis_obj.compute_analysis()
print(analysis_output)

# Analyze and plot data output matplotlib.Figure
analysis_figure = analysis_obj.plot_data()
analysis_figure = analysis_obj.plot_data("file_img.png")

# Notify the user that analysis is complete.
analysis_obj.notify_done("Test Message")

```
