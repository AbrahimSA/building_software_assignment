from Analysis import Analysis
import os 

def test_initial_value():
 # Verifies if all config from  configs/system_config.yml was load with success
   obj = Analysis('configs/system_config.yml')
   assert obj.config['ntfy_topic'] == "dsi_c2_brs"
   assert obj.config['ntfy_title'] == 'Building Robust Software Summative Assignment - Abrahim'
   assert obj.config['plot_color'] == 'white'
   assert obj.config['plot_title'] == 'Amount of Inspetion per met type'
   assert obj.config['plot_x_title'] == "Years"
   assert obj.config['plot_y_title'] == "Amount of Inspetion"
   assert obj.config['figure_width_size'] == 8
   assert obj.config['figure_height_size'] == 10
   assert obj.config['default_save_path'] == "plot_img.png"

def test_load_data():
     # Verifies dataset was load with success
    obj = Analysis('configs/system_config.yml')
    obj.load_data()
    assert obj.dataset is not None

def test_compute_analysis():
    # Verifies if  compute_analysis is returning the correct value
    obj = Analysis('configs/system_config.yml')
    obj.load_data()
    assert obj.compute_analysis() == 6.5

def test_plot_data():
    # Verifies if  file plot image was saved with success
    obj = Analysis('configs/system_config.yml')
    obj.plot_data("file_img.png")
    assert os.path.exists("file_img.png") == True

def test_notify_done():
    # Verifies if  message was delivered with success
    obj = Analysis('configs/system_config.yml')
    obj.notify_done("Test Message")
    assert obj.requests_status_code is not None
    status_code = obj.requests_status_code
    assert status_code == 200
