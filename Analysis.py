from typing import Any, Optional
import matplotlib.pyplot as plt
import pandas as pd
import yaml 
import requests
import os 
import statistics
import logging

logging.basicConfig(
level=logging.INFO,
handlers=[logging.StreamHandler(), logging.FileHandler('uci_iris.log')],
)
class Analysis():

    def __init__(self, analysis_config: str) -> None:
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
        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml']

        if not os.path.exists(analysis_config):
            raise ValueError("File  path does not exist! Could not load the configuration. Please try again.")


        # add the analysis config to the list of paths to load
        paths = CONFIG_PATHS + [analysis_config]

        # initialize empty dictionary to hold the configuration
        config = {}

        # load each config file and update the config dictionary
        for path in paths:
            logging.info('Loading data from {}'.format(path))
            try:
                with open(path, 'r') as f:
                        this_config = yaml.safe_load(f)
                config.update(this_config)
            except ValueError as e:
                logging.error('Error loading data from {}'.format(path), exc_info=True)
                e.add_node(f"Could not load the configuration from '{f}' file.")
        self.config = config

    def load_data(self) -> None:
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

        if self.config is None:
            raise ValueError("Config data not loaded. Can not load data from GitHub!")
        else:
            if 'gitHub_user' in self.config == False or  'gitHub_key' in self.config == False:
                raise ValueError("GitHub user config variables not set. Can not load data from GitHub !")

        try:
            logging.info('Loading data from {}'.format(self.config['gitHub_user']))
            url_path = 'https://api.github.com/users/' + self.config['gitHub_user'] + '/repos'
            data  = requests.get(url_path, auth=(self.config['gitHub_user'], self.config['gitHub_key']))
            self.dataset = data.json()
        except ValueError as err:
            logging.error('Error loading data from {}'.format(self.config['gitHub_user']), exc_info=True)
            err.add_node(f"Could not load data from gitHub. Unexpected {err=}, {type(err)=}.")

    def compute_analysis(self) -> float:
        '''Analyze previously-loaded data.

        This function runs an analytical meadian size of all repositories

        Parameters
        ----------
        None

        Returns
        -------
        analysis_output : float

        '''
        try:
            #Check if dataset is empty
            if self.dataset is not None:
                #Load all repository sizes
                sizes = [repo["size"] for repo in self.dataset] 
                #Calculate the repository meadian size
                median_size = statistics.median(sizes)
                print(median_size)
                return median_size
            else:
                raise ValueError("GitHub API data not loaded. Can not return the meadian size of repository!")
        except ValueError as err:
            err.add_node(f"Unexpected error! Unexpected {err=}, {type(err)=}.")

    def plot_data(self, save_path:str = None) -> plt.Figure:
        ''' Analyze and plot data

            Generates a plot, display it to screen, and save it to the path in the parameter `save_path`, or 
            the path from the configuration file if not specified.

            Number of head for cattle, calves, hogs, sheep and lamb from federally and provincially inspected slaughterhouses.

            Data Source:

            https://open.canada.ca/data/en/dataset/43ea3719-f2ea-4c30-91d2-c8cf9b9b1cef

            Federally Inspected Slaughter: Canadian Food Inspection Agency as compiled by Agriculture and Agri-Food Canada, Animal Industry Division, 
            except cattle and calves which is the Canadian Beef Grading Agency as compiled by Agriculture and Agri-Food Canada;

            Provincially Inspected Slaughter: Provincial Governments;

            Data lags 1-3 months.

            Parameters
            ----------
            save_path : str, optional
                Save path for the generated figure

            Returns
            -------
            fig : matplotlib.Figure

            '''
        
        if self.config is None:
            raise ValueError(f"Config not loaded! Can not plot data.")

        try: 
            red_meat_data = pd.read_csv('https://od-do.agr.gc.ca/MonthlyRedMeatSlaughter_AbattageAnimauxViandeRougeMensuelle.csv')
        except ValueError as err:
            err.add_node(f"Could not load data to plot. Unexpected {err=}, {type(err)=}.")

        try: 
            red_meat_data['EndDt_DtFin']  = red_meat_data['EndDt_DtFin'].astype('datetime64[ns]')
            red_meat_data['year']  = red_meat_data['EndDt_DtFin'].dt.year

            if 'figure_width_size' in self.config and  'figure_height_size' in self.config:    
                plt.figure(figsize=(self.config['figure_width_size'],self.config['figure_height_size']))
            
            fig, ax = plt.subplots()
            ax.set_axisbelow(True)
            ax.grid(alpha=0.8)
            ax.legend()
            ax.set_xlabel(self.config['plot_x_title'],fontsize = 10 )
            ax.set_ylabel(self.config['plot_y_title'],fontsize = 10)
            if self.config['plot_title']:
                plot_title = self.config['plot_title']
            else:
                plot_title = 'Amount of Inspetion per met type'

            if self.config['plot_color']:
                plot_color = self.config['plot_color']
            else:
                plot_color = 'blue'

            red_meat_data.groupby(['year', 'MjCmdtyFr_PrdtPrncplFr']).count()['NumHd_NmbTetes'].unstack().plot(ax=ax).set_title(plot_title)
            ax.get_legend().set_title("Meat Type")
            ax.set_facecolor(plot_color)
        except ValueError as err:
            err.add_node(f"Could not plot with data load. Unexpected {err=}, {type(err)=}.")

        try: 
            if save_path:
                plt.savefig(save_path)
            elif self.config['default_save_path']:
                plt.savefig(self.config['default_save_path'])
            else:
                print('Path to save the plot image not informed and default path is not avaialble! Plot file was not saved!')    
        except ValueError as err:
            err.add_node(f"Could not save plot image on path. Unexpected {err=}, {type(err)=}.")
        
        return(plt.figure)

    def notify_done(self, message: str) -> None:
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
        try:
            # Send a notification to the user through the ntfy.sh webpush service.
            resq = requests.post(
                'https://ntfy.sh/' + self.config['ntfy_topic'],
                data=message.encode('utf-8'),
                headers={'Title': self.config['ntfy_title']})
            self.requests_status_code = resq.status_code
            resq.close
            if self.requests_status_code == 200:
                print(f"Mensage delivered with success using '{self.config['ntfy_topic']}' ntfy.sh topic.")
            else:
                raise ValueError(f"Mensage was not deliver with success using '{self.config['ntfy_topic']}' ntfy.sh topic. Request status code: {self.requests_status_code}")

        except ValueError as err:
            err.add_node(f"Could not send mensage through ntfy.sh using '{self.config['ntfy_topic']}' topic. Unexpected {err=}, {type(err)=}.")