# 002 Technical Analysis

## Description
The objective of this project is to optimize a trading strategy using five technical indicators and compare its performance against a passive investment strategy. Different combinations of indicators were used, testing all possible combinations (2^5 - 1) to maximize key metrics such as the Sharpe Ratio, Max Drawdown, and Win-Loss Ratio.

## Technologies Used
- Python 3.12
- Libraries: NumPy, Pandas, Matplotlib, TA-Lib (or others specified in requirements.txt)

## Prerequisites
1. Python 3.12 installed on your machine.

## Installation Instructions

### Important Note

Before running the script, make sure to update the path in the code to point to your CSV file containing the data. Look for the line in main.py where the data is loaded, and modify the path accordingly:



## Steps for Windows:
1. Clone the repository:
   bash
   git clone https: //https://github.com/Kike14/Proyecto2

2. Create a virtual environment:
   bash
   python -m venv venv

3. Activate the virtual environment:
   bash
   .\venv\Scripts\activate
4. Upgrade pip:
   bash
   pip install --upgrade pip

5. Install dependencies:
   bash
   pip install -r technical_analysis\requirements.txt

6. Run the main script:
   bash
   python main.py

## Steps for Mac:
1. Clone the repository:
   bash
   git clone https://github.com/Kike14/Proyecto2
2. Create a virtual environment:
   bash
   python3 -m venv venv

3. Activate the virtual environment:
   bash
   source venv/bin/activate

4. Upgrade pip:
   bash
   pip install --upgrade pip

5. Install dependencies:
   bash
   pip install -r technical_analysis/requirements.txt

6. Run the main script:
   bash
   python main.py

## Project Structure
your_project/
│
├── technical_analysis/
│   ├── _main_.py
│   └── requirements.txt
├── README.md

## Contributing
Contributions are welcome. Please submit a pull request following the style guidelines and best practices.

## License