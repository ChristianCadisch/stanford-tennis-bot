# Stanford West Campus Tennis Court Reservation Bot 🎾🤖

![bot](https://github.com/ChristianCadisch/stanford-tennis-bot/blob/main/Image.jpg)

## Purpose

This project is designed to automate the reservation process for tennis courts at Stanford’s West Campus. The bot logs into the Club Locker website, navigates to the reservations page, and selects the ideal time slots (prioritizing times after 6 PM). The script uses Selenium for web automation and can be customized to move a specified number of days ahead to make future reservations.

### Prerequisites

* Login to Stanford's Club Locker System
* Python 3.6 or higher
* Google Chrome browser
* ChromeDriver (compatible with your version of Chrome)

## Installation
### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/tennis-court-reservation.git
cd tennis-court-reservation
```

### Step 2: Set Up Virtual Environment

For macOS and Linux:
```bash
python3 -m venv .env
source .env/bin/activate
```

For Windows:
```bash
python -m venv .env
.env\Scripts\activate
```
### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```
### Step 4: Download ChromeDriver

Download ChromeDriver from the official [ChromeDriver download page](https://sites.google.com/chromium.org/driver/downloads). Choose the version that matches your installed version of Google Chrome.
Extract the downloaded file and move it to a location in your system’s PATH or specify its location in the script.

### Step 5: Adust auth.json File
Add your Club Locker login info to the auth.json file in the project directory:

### Step 6: Make the Bash Script Executable (macOS and Linux)
```bash
chmod +x run_reserve.sh
```
### Step 7: Running the Script 🎉
Just double click on the run_reserve.sh file 🪄


## Notes

* The script prioritizes reservation slots after 6 PM (6:00 PM, 7:00 PM, 8:00 PM). If these slots are unavailable, it will attempt to reserve earlier slots.
* Ensure your chromedriver path is correctly specified in reserve.py.

### Troubleshooting

If you encounter any issues, ensure that:

* The auth.json file contains correct login credentials.
* ChromeDriver is compatible with your installed version of Google Chrome.
* The virtual environment is activated before running the script.

Feel free to open an issue on the GitHub repository if you have any questions or run into problems.

