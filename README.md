# CoinAPI

This service collects data from a cryptocurrency exchange, and serves them via a fastAPI API.

## Installation

First, clone the repository.

 ```bash
 git clone 'https://github.com/MarkusMusch/CoinAPI.git' && cd CoinAPI/
 ```

Second, install all necessary dependencies by calling:

 ```bash
 poetry install
 ```

## Usage

For permanent usage, the application comes with a Docker file to build a Docker container.

To build the container run:

 ```bash
 sudo docker build -t coinapi .
 ```

 To start the container run:

 ```bash
 sudo docker run -d -p 8000:8000 --name coinapi-container --restart unless-stopped coinapi
 ```

 This starts the container on Port 8000.

 The --restart option when starting the container makes the container start every time you boot your computer. Since the app is downloading the newest data upon starting, it can take a few moments until the app is available in the browser after booting your system.

## Contributing

1. Fork it (https://github.com/MarkusMusch/CoinAPI/fork)
2. Create your feature branch (git checkout -b feature/fooBar)
3. Commit your changes (git commit -am 'Add some fooBar')
4. Push to the branch (git push origin feature/fooBar')
5. Create a new Pull Request

## License and author info

### Author

Markus Musch

### License

See the [LICENSE](LICENSE.txt) file for license rights and limitations (GNU GPLv3).
