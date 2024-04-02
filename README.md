## About

This project provides a framework with which you can manage your browser using a daemon script.

What this Project Does:
- provides automatic login function for a 360 home router (reverse-engineered from the javascript)..
- logs network activity of users (by scraping the router's management page).
- plots a user's activity.
- implements a flask server to disply the plotted graphs.

Structure of the files:

<img src="https://github.com/mindcrunch4u/home_router_management/blob/main/about/about%20files.png" width="500">

An example of served graphs (plotted using the information gathered from `info.py`):

<img src="https://github.com/mindcrunch4u/home_router_management/blob/main/about/screenshot%20example.png" width="500">

## Using this Project

1. Copy `systemd/info.service` to `/etc/systemd/system/info.service`
	- Update `ExecStart` to point to the path of the `info.py` script.
2. Copy `systemd/dataexpo.service` to `/etc/systemd/system/dataexpo.service`
	- Update `ExecStart` to point to the path of the `dataexpo.py` script.
3. Start the services
	- `systemctl restart info` # to collect information.
	- `systemctl restart dataexpo` # to plot the collected information.

Visit `127.0.0.1:8081` to view the plots.

## Using a Different Router

If you are using a different router, you must implement the following parts yourself in `info.py`:
- `calculate_crypt_string()`: depends on your router's management routine.
- `refresh_header()`: depends on your router's login link.
- `cleanup_procedure()`: this changes the access token when the older one expires.
- `main()`: you have to change the endpoint of the router's management page.
