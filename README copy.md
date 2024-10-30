# Music Data Exporter

#### Video Demo: <https://youtu.be/-AH5V9su25k)>

#### Description:

The Music Data Exporter is a Python application designed to help music enthusiasts retrieve their top albums from Last.fm, a widely used music tracking service. By utilizing the Last.fm API, users can effortlessly access their listening data, which can be exported in either CSV or JSON formats. This project combines elements of API interaction, data processing, and user input handling to create a user-friendly experience.

**Project Structure:**

The project contains the following files:

1. **`project.py`**: This is the main script that drives the application. It contains the primary logic for loading user configuration, fetching top albums from the Last.fm API, and exporting that data. The script is structured into several key functions:
   - `load_config()`: This function loads user configuration from a JSON file. If the configuration file does not exist or lacks necessary information, it calls `setup_config()` to prompt the user for their Last.fm API key, username, and preferred export settings.
   - `setup_config()`: This function is responsible for guiding the user through the configuration setup process. It collects essential information and saves it to `config.json`, allowing for easy access in future sessions.
   - `fetch_top_albums(api_key, username)`: This function interacts with the Last.fm API to retrieve the user's top albums. It handles API requests and parses the response to extract relevant album information.
   - `main()`: The main function orchestrates the execution of the application by calling the necessary functions to load configuration, fetch data, and display the results to the user.

2. **`test_project.py`**: This file contains unit tests for the functions defined in `project.py`. Using the pytest framework, the tests verify the correctness of the application’s functionalities. Key tests include:
   - `test_load_config()`: Verifies that configuration loading works as expected, including handling missing or incomplete configuration files.
   - `test_setup_config()`: Tests the configuration setup process to ensure user inputs are correctly saved.
   - `test_fetch_top_albums()`: Mocks API calls to confirm that the function correctly fetches and processes data from Last.fm.

3. **`config.json`**: This file is created automatically during the configuration setup. It stores the user’s Last.fm API key, username, export format preference, and export location, ensuring that users do not need to re-enter their information each time they run the application.

4. **`requirements.txt`**: This file lists the dependencies required for the project. Currently, the application relies on the `requests` library for handling HTTP requests to the Last.fm API. Users can easily install these dependencies using pip.

**Design Choices:**

During the development of the Music Data Exporter, several design choices were made to enhance usability and functionality. The decision to utilize a configuration file (config.json) allows for a more streamlined user experience by saving essential user inputs, eliminating the need for repetitive data entry. Additionally, providing export options (CSV and JSON) caters to different user needs, enabling easy data analysis or archiving.

The application is designed with error handling in mind. If the API request fails, users receive a clear error message, guiding them to check their credentials. This emphasis on user feedback is crucial for ensuring a smooth experience.

Moreover, the choice to implement unit tests using pytest was driven by the need for reliable code. Automated testing ensures that any future changes or enhancements do not introduce bugs, thus maintaining the integrity of the application.

**Conclusion:**

The Music Data Exporter is a robust tool that empowers users to manage their music data effectively. By leveraging the Last.fm API and providing flexible export options, the project not only showcases the capabilities of Python programming but also emphasizes good software design principles such as user feedback, error handling, and maintainability through testing. This project stands as a testament to the integration of practical programming skills with a passion for music, offering a valuable resource for anyone looking to analyze their listening habits.
