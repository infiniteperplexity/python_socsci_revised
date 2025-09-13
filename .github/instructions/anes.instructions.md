---
applyTo: '**'
---
This repo contains code and data related to the American National Election Studies (ANES) time series datasets.  The raw cumulative file through 2020 has been downloaded, and so have the single-year time series data sets for 2000-2024.  Work is now underway to build a harmonized data set for 2000-2024.

One of the most common requests you will get is to answer questions about the variables and documentation.  Most of the text documents are very long, so the best approach will usually be to search for relevant keywords and extract surrounding text.  For many cases, it will be enough to search the /raw/variable_guides txt files.  For more complex questions, it may be necessary to search the actual codebooks, which are currently in /raw/txt/.

If it is necessary to look at the actual data files, you can use the run_pandas_code_tool to inspect the distribution of values for a variable.  Avoid doing so unless it is necessary or requested, because it will be time-consuming to convert the unharmonized data.