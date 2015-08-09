# ohio-voter-analysis
### Infer party affiliation based on voting history

The Ohio Secretary Of State provides a [comprehensive data set](http://www2.sos.state.oh.us/pls/voter/f?p=111:1) of Ohio voter registration and voting history. **ohio-voter-analysis** attempts to parse that data to infer which party a voter is likely to support. Some of this is easy, as many voters are registered to a specific party. Many, however, are not. But this information can be inferred based on which primary in which a voter participates. **ohio-voter-analysis** uses this as an additional heuristic for its inference. Obviously, affiliation and history is no guarantee of how someone will vote in a future election. *Note*: Ohio has something known as a [semi-open primary](https://www.sos.state.oh.us/sos/elections/Voters/FAQ/genFAQs.aspx#declare) system.

## Usage

Run this:

```sh
git clone git@github.com:hodgesmr/ohio-voter-analysis.git ~/ohio-voter-analysis
python ~/ohio-voter-analysis/analyze.py
```

The script will guide you through downloading, parsing, and analyzing the data. Output data is dumped to `ohio-voter-analysis/data/`.

## A Matt Hodges project

This project is maintained by [@hodgesmr](http://twitter.com/hodgesmr).
