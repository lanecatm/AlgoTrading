cd ../algo_trading/
echo algoTradingUnitTest
python algoTradingUnitTest.py | grep error
echo repoForATUnitTest
python repoForATUnitTest.py | grep error
cd ../common/
#echo MarketDataUnittest
#python MarketDataUnittest.py | grep error
cd ../pool/
echo poolFromSinaApiUnitTest
python poolFromSinaApiUnitTest.py| grep error
echo tradingRecordSaverUnitTest
python tradingRecordSaverUnitTest.py | grep error
cd ../quant_analysis/
echo LinearVWAPQuantAnalysisUnitTest
python LinearVWAPQuantAnalysisUnitTest.py| grep error
echo TWAPQuantAnalysisUnitTest
python TWAPQuantAnalysisUnitTest.py| grep error
echo VWAPQuantAnalysisUnitTest
python VWAPQuantAnalysisUnitTest.py| grep error
echo quantAnalysisBaseUnitTest
python quantAnalysisBaseUnitTest.py| grep error
cd ..
