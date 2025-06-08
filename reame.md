C:\geekom_python_projects\git_projects\chart_viewer
cd /mnt/c/geekom_python_projects/git_projects/chart_viewer

python3 -m venv .venv
source .venv/bin/activate  
# .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Step into your project directory
cd /mnt/c/geekom_python_projects/git_projects/<your_project>

# Step 1: Initialize Git (if not done already)
git init

# Step 2: Add and commit
git add .
git commit -m "Initial commit for Render"

# Step 3: Ensure branch is named 'main'
git branch -M main

# Step 4: Add remote (if not already added)
git remote add origin git@github.com:ofukushi/<your_repo_name>.git 2>/dev/null || \
git remote set-url origin git@github.com:ofukushi/<your_repo_name>.git

🚀 If Repo Doesn’t Exist Yet
Then replace Step 4 with:
bash
gh repo create <your_repo_name> --public --source=. --push
gh repo create umineko_db_pool --public --source=. --push
gh repo create uweb_11 --public --source=. --push

# Step 5: Push to GitHub
git push -u origin main


We now have a working Flask app that:
    Authenticates and fetches data from JQuants API.
    Saves weekly margin interest into Postgres if not present.
    Pulls daily price data and combines both into a Plotly chart.
    Renders an index page with a stock code input and chart output.

🟩 Top Section — Candlestick Chart (Price)
This displays daily stock prices over the last 3 years:
    Each bar (candle) represents a single day.
    Green candles = stock closed higher than it opened (up day).
    Red candles = stock closed lower than it opened (down day).
    The wicks show the high/low of the day.
    The body shows the open/close range.
This gives a visual view of volatility, trends, and price ranges.

🟦 Overlay Line — Weekly Margin Interest (Right Axis)
    This line represents LongMarginTradeVolume for the same stock.
    It's plotted on the right Y-axis ("Margin Volume").
    Peaks in the line mean many investors are using credit (margin) to buy this stock.
    Dips may signal selling or reduced interest in leveraging.

🕰️ X-Axis — Date
    Time progresses left to right over a 3-year window.
    Helps correlate price movements with shifts in investor margin behavior.

📊 Example Insights You Can Extract:
    Did large increases in margin interest precede a rally or drop?
    Are there recurring seasonal spikes in credit usage?
    When volume surged, did price trend up or down?

The reason your utils/fetch.py and utils/auth.py can access the .env values without calling load_dotenv() themselves is because:
✅ load_dotenv() is process-wide
Once load_dotenv() is called anywhere in the application (e.g., app.py), it loads the variables from the .env file into the global environment (os.environ), and these are accessible from all modules in the same process.
📌 What’s happening:
    app.py runs first and executes:
from dotenv import load_dotenv
load_dotenv(dotenv_path=".../.env.chart_viwer")
This populates os.environ globally.
When other modules like utils/fetch.py or utils/auth.py do:
os.getenv("G_MAIL_ADDRESS")
It works because os.environ is already populated.