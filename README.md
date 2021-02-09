# Python CLI  structure

This command line project is written in python3 and is using to retrieve data and analyze financial data available on https://finnhub.io website. Also please consider that for graphing, “plotille” library in python is being used. For printing the requested results, it uses standard STDOUT and STDERR in sys libyrary, To get make the request via API to finnhub website it uses “requests” library, for changing timing for each stock and quotes “datetime” library, “unittest” library for write the unit test part and other standard libraries like pandas, math, numpy.

To start the application use below command in the “pycli-master” directory to automatically install the application.
pip install e .

For running the unit test use below line in “pycli-master\clistock” directory:
python -m unittest test_funcmodule.py
which will result as:
 
# Commands:
To use the application below please consider to use following commands:

- To draw a graph in terminal for a stock with given time interval use below lines. In case end time of interval is not specified the application uses automatically the present time. Time and symbol is optional and could be defined by user but timing convention should be as examples below.
+ clistock time_stock_graph AAPL 2019-02-02
+ clistock time_stock_graph AAPL 2019-02-02 2020-02-02
 

- Also following line to make the graph for exchange historical data:
+ clistock graph_hist_fx OANDA:GBP_USD

- To draw a graph based on the whole historical data of a stock with exchange affect following examples could be used. In case no exchange give, it uses the current values in USD:
+ clistock graph_hist_stock AAPL OANDA:GBP_USD

- Also following line to make the graph for exchange historical data:
+ clistock graph_hist_fx OANDA:GBP_USD

to convert and print historical stock quotes in given foreign currencies:
+ clistock print_historical AAPL OANDA:GBP_USD


