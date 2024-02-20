# Sitting Duration Calculator

## Overview

This repository contains Python code for calculating the duration of sitting based on the API data from a location sensor. The sensor provides information about a person's movement in a room, and this code processes the data to determine the total time spent in a designated sitting area.

## Usage

### Prerequisites

- Docker installed: [Get Docker](https://docs.docker.com/get-docker/)

### Setup

1. **Clone the Repository:**

    ```bash
    git clone git@github.com:noaamaman325158/VayyarHomeTaskNoaaMaman.git
    cd sitting-duration-calculator
    ```

2. **Install Dependencies:**

    ```bash
    # If using virtual environment
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
    ```

    ```bash
    # Install dependencies
    pip install -r requirements.txt
    ```

3. **Build the Docker Image:**

    ```bash
    docker build -t noaa13092/sitting_duration_calculator .
    ```

4. **Run the Docker Container:**

    ```bash
    docker run -p 4000:80 noaa13092/sitting_duration_calculator:latest
    ```

5. **Access the Service:**

    Open a web browser and navigate to [http://localhost:4000](http://localhost:4000).

## API Documentation

- The sensor API provides endpoints for retrieving data related to a person's movement in the room.
- Detailed API documentation can be found [here](#) (replace # with the actual link to your documentation).

## Calculating Sitting Duration

To calculate the sitting duration, the code processes the data from the sensor API. The results are displayed in the console or any defined output format.

## Contributing

If you would like to contribute to this project, please follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
