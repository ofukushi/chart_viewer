
can you make a code that do the following?
Access Jquants api and get histtorical stock prices and weekly_margin_interest.
Draw graph which consists of daily stock price bar charts, candle stick or ohlc, and line which shows weekly_margin_interest.
The graph has two parts upper portion shows stock charts, and the bottom portion shows. Or they can be combined.
time fram of the graph is 3 years long.
Stock price data will be fetched every time the charts is depict, but weekly_margin_interest data should be saved in table "weekly_margin_interest" in the folloing DB, and depicted from woth using that data.
mk table logic is needed if table does not exist. 
Databese selection logic is necessary.
This will be developed by Flask app.
indexx page will have box where company code will be probided and a grapf for that company will be rendered.
Is there any necessary info ? Or any Questions?

DB credentials:
HEROKU_DATABASE_URL=postgres://u4gfsf6lr4e5sj:p37e834285e1c5161de955adf23c5304df5878d00cb78847100ffac916c995840@ceqbglof0h8enj.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d1kmc11fnhb6np
LOCAL_DB_URL=postgresql://postgres_ubuntu:55@localhost:5432/postgres_ubuntu_db

API references:
G_MAIL_ADDRESS=o.fukushi@gmail.com
J_QUANTS_PASSWORD=7HKhUci36SBk4qX

Refresh token can be obtained using your registered email and password.
{
    "refreshToken": "<YOUR refreshToken>" 
}
import requests
import json

data={"mailaddress":"<YOUR EMAIL_ADDRESS>", "password":"<YOUR PASSWORD>"}
r_post = requests.post("https://api.jquants.com/v1/token/auth_user", data=json.dumps(data))
r_post.json()

The ID token can be obtained using the refresh token obtained on the sign in page.
{
    "idToken": "<YOUR idToken>" 
}
import requests
import json

REFRESH_TOKEN = "YOUR refreshtokenID"
r_post = requests.post(f"https://api.jquants.com/v1/token/auth_refresh?refreshtoken={REFRESH_TOKEN}")
r_post.json()

Listed Issue Information (/listed/info)
You can get information on listed companies and sector information
{
    "info": [
        {
            "Date": "2022-11-11",
            "Code": "86970",
            "CompanyName": "日本取引所グループ",
        　　　　　　　　"CompanyNameEnglish": "Japan Exchange Group,Inc.",
            "Sector17Code": "16",
            "Sector17CodeName": "金融（除く銀行）",
            "Sector33Code": "7200",
            "Sector33CodeName": "その他金融業",
            "ScaleCategory": "TOPIX Large70",
            "MarketCode": "0111",
            "MarketCodeName": "プライム",
            "MarginCode": "1",
            "MarginCodeName": "信用",
        }
    ]
}
import requests
import json

idToken = "YOUR idToken"
headers = {'Authorization': 'Bearer {}'.format(idToken)}
r = requests.get("https://api.jquants.com/v1/listed/info", headers=headers)
r.json()



Historical stock prices including both adjusted and unadjusted prices, taking into account stock splits, etc.
Stock price consists before and after adjustment of stock splits and reverse stock splits (Rounded to first decimal places)
Attention
    Open, High, low, close, the volume of trade and the amount of purchase for the issue on the day when there is no trade volume (no sale) are recorded as Null.
    Stocks that are not listed on the TSE (including issue listed only on the other exchanges) are not included in the data.
    The data for Oct. 1st, 2020 are the OHLC, trading volume, and trading value in Null because trading was halted all day due to the failure of the equity trading system, arrowhead.
    Daily prices can be obtained for all plans, but morning/afternoon session prices are available only for premium plan.
    Stock price adjustments are supported only for stock splits and reverse stock splits. Please note that some corporate actions are not supported.
{
    "daily_quotes": [
        {
            "Date": "2023-03-24",
            "Code": "86970",
            "Open": 2047.0,
            "High": 2069.0,
            "Low": 2035.0,
            "Close": 2045.0,
            "UpperLimit": "0",
            "LowerLimit": "0",
            "Volume": 2202500.0,
            "TurnoverValue": 4507051850.0,
            "AdjustmentFactor": 1.0,
            "AdjustmentOpen": 2047.0,
            "AdjustmentHigh": 2069.0,
            "AdjustmentLow": 2035.0,
            "AdjustmentClose": 2045.0,
            "AdjustmentVolume": 2202500.0,
            "MorningOpen": 2047.0,
            "MorningHigh": 2069.0,
            "MorningLow": 2040.0,
            "MorningClose": 2045.5,
            "MorningUpperLimit": "0",
            "MorningLowerLimit": "0",
            "MorningVolume": 1121200.0,
            "MorningTurnoverValue": 2297525850.0,
            "MorningAdjustmentOpen": 2047.0,
            "MorningAdjustmentHigh": 2069.0,
            "MorningAdjustmentLow": 2040.0,
            "MorningAdjustmentClose": 2045.5,
            "MorningAdjustmentVolume": 1121200.0,
            "AfternoonOpen": 2047.0,
            "AfternoonHigh": 2047.0,
            "AfternoonLow": 2035.0,
            "AfternoonClose": 2045.0,
            "AfternoonUpperLimit": "0",
            "AfternoonLowerLimit": "0",
            "AfternoonVolume": 1081300.0,
            "AfternoonTurnoverValue": 2209526000.0,
            "AfternoonAdjustmentOpen": 2047.0,
            "AfternoonAdjustmentHigh": 2047.0,
            "AfternoonAdjustmentLow": 2035.0,
            "AfternoonAdjustmentClose": 2045.0,
            "AfternoonAdjustmentVolume": 1081300.0
        }
    ],
    "pagination_key": "value1.value2."
}
import requests
import json

idToken = "YOUR idToken"
headers = {'Authorization': 'Bearer {}'.format(idToken)}
r = requests.get("https://api.jquants.com/v1/prices/daily_quotes?code=86970&date=20230324", headers=headers)
r.json()

Margin Trading Outstandings (/markets/weekly_margin_interest)
Weekly margin trading outstandings is available.
{
    "weekly_margin_interest": [
        {
            "Date": "2023-02-17",
            "Code": "13010",
            "ShortMarginTradeVolume": 4100.0,
            "LongMarginTradeVolume": 27600.0,
            "ShortNegotiableMarginTradeVolume": 1300.0,
            "LongNegotiableMarginTradeVolume": 7600.0,
            "ShortStandardizedMarginTradeVolume": 2800.0,
            "LongStandardizedMarginTradeVolume": 20000.0,
            "IssueType": "2"
        }
    ],
    "pagination_key": "value1.value2."
}
import requests
import json

idToken = "YOUR idToken"
headers = {'Authorization': 'Bearer {}'.format(idToken)}
r = requests.get("https://api.jquants.com/v1/markets/weekly_margin_interest?code=86970", headers=headers)
r.json()

Outstanding Short Selling Positions Reported (/markets/short_selling_positions)
You can get the outstanding short selling positions reported data.
{
    "short_selling_positions": [
      {
        "DisclosedDate": "2024-08-01",
        "CalculatedDate": "2024-07-31",
        "Code": "13660",
        "ShortSellerName": "個人",
        "ShortSellerAddress": "",
        "DiscretionaryInvestmentContractorName": "",
        "DiscretionaryInvestmentContractorAddress": "",
        "InvestmentFundName": "",
        "ShortPositionsToSharesOutstandingRatio": 0.0053,
        "ShortPositionsInSharesNumber": 140000,
        "ShortPositionsInTradingUnitsNumber": 140000,
        "CalculationInPreviousReportingDate": "2024-07-22",
        "ShortPositionsInPreviousReportingRatio": 0.0043,
        "Notes": ""
      }
    ],
    "pagination_key": "value1.value2."
}
import requests
import json

idToken = "YOUR idToken"
headers = {'Authorization': 'Bearer {}'.format(idToken)}
r = requests.get("https://api.jquants.com/v1/markets/short_selling_positions?code=86970&calculated_date=20240801", headers=headers)
r.json()


