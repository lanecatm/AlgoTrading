集思广益  大家想下
#FSC Final Presentation (5 min)

## Introduction
- Algorimthic Trading System Definitoin

## System Design
- Python 
- MySQL
 
```
AlgoTraidng
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

## Features
- Volume Prediction
- Active Trading Strategy
- Realtime Pool / Back-test Pool/ Internal Pool
- Data 
- Monitor
- GUI & CLI
- Fully Tested
- Informative Log

# Demo (10 min)
1. GUI
2. Place Order
3. 
