集思广益  大家想下
#FSC Final Presentation (5 min)

## Introduction
- Algorimthic Trading System Definitoin

## System Design / Components
- Python 
- MySQL
 
```
AlgoTrading
├── algo_trading  
│   ├── algoTrading.py
│   └── repoForAT.py
├── cli
│   └── cli.py
├── common
│   ├── MarketData.py
│   ├── clientOrder.py
│   ├── orderResult.py
│   └── tradingUnit.py
├── fetch_data
│   ├── changeDataFromSqliteToMysql.py
│   ├── marketDataGetter.py
│   └── repo.py
├── pool
│   ├── poolBase.py
│   ├── poolFromSinaApi.py
│   └── tradingRecordSaver.py
├── quant_analysis
│   ├── LinearVWAPQuantAnalysis.py
│   ├── TWAPQuantAnalysis.py
│   ├── VWAPQuantAnalysis.py
│   └── quantAnalysisBase.py
└── tool
    ├── ErrorCode.py
    ├── FigHelper.py
    ├── FileHelper.py
    ├── FileUtility.py
    └── Log.py
```

## Challanges & Solutions
- Data feed
	* crawl market data
	* sqlite to MySQL
- Trading Strategy

## Features
- Volume/Price Prediction
- Active Trading Strategy / Frequency adjusts
- Both market order and limit order supported
- Realtime Pool / Back-test Pool / (Internal Pool)
- Data feed
- Monitor
- GUI & CLI
- Unit Tests
- Informative Log

# Demo (10 min)
1. GUI
2. Start algoTrading
2. Place pruchase order
3. Execute order
4. 
