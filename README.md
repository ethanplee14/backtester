BackTester for options using orats data

### TODO
- [x] Refactor options data to their own OptionsDoc, OptionsChain and Options models
- [x] Implement multiprocessing pool to utilize full capabilities of computer's resources to process data
- [ ] Refactor fetch_data method into a class to connect to the mongodb instance once and fetch data using a single MongoClient instance
- [ ] Implement multithreaded pool to submit tasks to request mongodb data and then queue the data for analysis.
- [ ] Refactor IronCondor trade to be it's own model that holds the Options in it's legs.