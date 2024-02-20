# Sitting Duration Calculation

## Overview

This repository contains Python code for calculating the duration of sitting based on the API data from a location sensor. The sensor provides information about a person's movement in a room, and this code processes the data to determine the total time spent in a designated sitting area.
## Usage

### Prerequisites

- Docker installed: [Get Docker](https://docs.docker.com/get-docker/)

### Setup

1. **Clone the Repository:**

    ```bash
    git clone git@github.com:noaamaman325158/VayyarHomeTaskNoaaMaman.git
    cd mock-api-sensor
    ```

2. **Build the Docker Image:**

    ```bash
    docker build -t noaa13092/mock_api_sensor .
    ```

3. **Run the Docker Container:**

    ```bash
    docker run -p 4000:80 noaa13092/mock_api_sensor:latest
    ```

4. **Access the Service:**

    Open a web browser and navigate to [http://localhost:4000](http://localhost:4000).

## API Documentation

- The sensor API provides endpoints for retrieving data related to the person's movement in the room.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
