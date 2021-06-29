# Meteostat Server

The Meteostat server allows everyone to run a local instance of the Meteostat [JSON API](https://rapidapi.com/meteostat/api/meteostat/). The server provides different endpoints which return historical weather data and meta information in JSON format.

## Installation

First, make sure you have Git and Python 3 running on your machine.

Then, clone this repository by running:

```sh
git clone https://github.com/meteostat/meteostat-server
```

Now you can install the package's dependencies:

```sh
cd meteostat-server
python3 -m pip install . -U
```

Finally, you can run a local test server using:

```sh
python3 app.py
```

## Deployment

When deploying Meteostat Server for production, you should use a robust web server like Apache or nginx. Generally, the process is as straight-forward as deploying any other Flask application.

### Apache

At Meteostat we're using Apache on Ubuntu. The Apache server is running using the `app.wsgi` file provided in this repository.

First, let's install `mod_wsgi`:

```sh
apt-get install libapache2-mod-wsgi-py3
```

Then, add an Apache configuration file using this template:

```
ServerName jasper.meteostat.net
WSGIScriptAlias / /var/www/vhosts/jasper.meteostat.net/meteostat-server/app.wsgi
```

If you're receiving internal server errors when accessing endpoints, please check if the Apache user has write-access for Meteostat Python's cache directory. You can grant missing rights using `chmod`:

```sh
sudo chmod -R 777 /var/www/
```

Also, after making changes to the Python code or pulling the latest state, you'll probably need to restart Apache for the changes to become effective:

```sh
/etc/init.d/apache2 restart
```

## Data License

Meteorological data is provided under the terms of the [Creative Commons Attribution-NonCommercial 4.0 International Public License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/legalcode). You may build upon the material
for any purpose, even commercially. However, you are not allowed to redistribute Meteostat data "as-is" for commercial purposes.

## Code License

The code of the Meteostat project is available under the [MIT license](https://opensource.org/licenses/MIT).
