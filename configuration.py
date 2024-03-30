
class DefaultConfig:
    def __init__(self):
        self.plot_host_name = "" # when plotting, the script looks for this hostname, and generates a plot for this machine. Other machines are ignored, but it is possible to generate plots for them as well. You just have to update the hostname here, and run the script again.
        self.log_file_path = "" # the log files are JSON responses returned from the router, they (the log files) are the data source for generating plots. This variable points to the log files.
        self.img_file_path = "" # the output folder for the plots, which will be used by the web server to serve plot history to the user.

default_config = DefaultConfig()
default_config.plot_host_name = "Xiaomi-Civi-3"
default_config.log_file_path = "/root/scripts/log*.txt" 
default_config.img_file_path = "/root/scripts/dataexpo/images/"

default_config.router_username = "admin"
default_config.router_ivstring = "360luyou@install"
default_config.router_password = "abcd6666"
