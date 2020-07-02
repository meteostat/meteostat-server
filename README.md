# API
This repository contains the code for the new Meteostat API which will be written in Python.

## Contributing
Meteostat is a voluntary initiative that fosters open source. We rely on coding enthusiasts who are passionate about meteorology to grow our database and make weather and climate data available to everyone.

## Roadmap
To get this project started we will first need to develop a base class that handles the database connection and produces uniform JSON output. Once this is done we can start rewriting existing PHP endpoints in Python.

After the current state is reproduced in Python we can focus on improving point data output with machine learning.

## Legacy Code
Meteostat started as a beginner's coding project, written in PHP, and developed into a large platform for weather statistics. As thousands of users are starting to use the project's web application and API, Meteostat needs to shift its amateur code base to a more professional setup. We decided to go with Python due its popularity and the great ability to work with large amounts of data. However, our legacy PHP code is still available in an [archived repository](https://github.com/meteostat/api-legacy). You can use the PHP scripts in this repository as an inspiration for your Python implementations.

## Testing
For now we will only do manual testing. However, a proper strategy for code testing will be defined in the near future.

## License
The code of the Meteostat project is available under the [MIT license](https://opensource.org/licenses/MIT).
