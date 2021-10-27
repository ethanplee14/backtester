### Overview
Algorithmic strategy back tester using daily Open, High, Low, Close, Adjusted, Volume (ohlcav) options supplied 
and formatted from ORATS and daily ohlcav stock data.  

### Project Structure
- Data - A module with a fetch_data method. Implementation is `data/HistoricalFetcher` which fetches options data from 
`orats/OratsDb` for a MongoDB and stock data from daily_ohlcv_period method in the `data/yahoo/yahoo_fetch` to get 
stock ohclv.
- Strategy - Runs a strategy to see if it should make a trade with the given passed in data. Only strategy developed so 
far is located at `strategies/ic_nope/__init__`. The ICNope strategy takes a weekly NOPE calculation which is the 
ratio of the summation of all option delta over volume. If Nope is high, place an IronCondor option trade.
- Strategy Launcher - Verifies and normalizes passed in daily fetched data, then launches the strategy.
- TradeAnalyze - Module to make final analysis and calculations to the trade. For the ICNope strategy, 
`analytics/ICTradeAnalyzer` calculates premiums and profits made from the strategy.  
- EngineProcess - Processes a back test by tying together the Data, StrategyLauncher, and Analyzer. Originally used 
`simulators/processes/StrategyProcess` which fetches the entire dataset before running the strategy. This created a 
lot of space complexity as OptionDocs are large and running it over the course of a few years with multiple tickers is 
too intensive. In order to fix this, implemented a `simulators/process/StreamedStrategyProcess` to stream data from the 
database that way we don't need to hold onto un-necessary data. 
- StrategyEngine - Runs the EngineProcess. Originally implemented a `simulator/engine/LinearEngine` which completely 
eliminates the needs for an EngineProcess as it runs each ticker's back test one at a time. Iteratively processing 
each ticker's back test created a lot of time complexity. Network requests and iteratively processing each day's data 
and trade is slow. To fix this, I implemented a `simulator/engine/StrategyEngine` which utilizes multiprocessing. 
Python's multithreading doesn't allow for continuous computational analysis due to python's GIL. Since multithreading is 
for concurrency while multiprocessing is used for parallelism and information doesn't need to be shared between 
processes, multiprocessing was a good fit for the new engine. 
- Simulator - Simulates a portfolio with a balance and held positions. Runs the passed in engine and updates the portfolio
based on the engine's trade results. `simulator/WeightedSimulator` implements a weighted portfolio simulation where
you can pre-define a ticker's weight in a portfolio. In the `./main` file currently using equal distribution.


### TODO
- [x] Refactor options data to their own OptionsDoc, OptionsChain and Options models
- [x] Implement multiprocessing pool to utilize full capabilities of computer's resources to process data
- [X] Refactor fetch_data method into a class to connect to the mongodb instance once and fetch data using a single MongoClient instance
- [X] Implement multithreaded pool to submit tasks to request mongodb data and then queue the data for analysis.
- [X] Refactor IronCondor trade to be its own model that holds the Options in its legs.
- [X] Develop Simulator Engine for running strategies while streaming mongodb data, rather than storing.
- [X] Implement Logging for strategy pool to flexibly manage output
- [ ] Create Analyzer Module to string various analysis together.

### Caveats
This project was made for personal use. Design was an important consideration for a flexible system, but it lacks 
comments/documentation. Testing coverage is roughly 30-40%, mostly for mathematical calculations. Integration 
tests were done manually and final results were carefully evaluated to ensure the back test's reliability.    
