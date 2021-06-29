# Meteostat Server

The Meteostat server allows everyone to run a local instance of the Meteostat [JSON API](https://rapidapi.com/meteostat/api/meteostat/). The server provides different endpoints which return historical weather data and meta information in JSON format.

**Important:** This package is work in progress. Do not use it in production.

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

## License

The code of the Meteostat project is available under the [MIT license](https://opensource.org/licenses/MIT).
