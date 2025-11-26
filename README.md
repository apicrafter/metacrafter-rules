# metacrafter-rules
Extended set of rules for metacrafter metadata identification and classfication tool.

Additional rules include:
- Russian government, geo, codes, orgs, persons, government finances codes
- German date time and geo
- Spanish PII codes
- Set of extended rules to identify date time, common objects, internet codes


## How to use?

1. Pull code with `git clone https://github.com/apicrafter/metacrafter-rules`
2. Install it `python3 setup.py install`
3. Create file `.metacrafter` in current directory or in user root directory and add rulepath attribute

Windows example of the _.metacrafter_ file
```yaml
rulepath:
   - C:\workspace\public\apicrafter\metacrafter-rules\rules\ 
```

## How it works

Some of extended rules use Python functions to validate columns names and column values. These valudation functions accept string or any value and return boolean. 

For example `metacrafterext.rules.en.orgs.is_us_orgname` function validates that string is a US company. 

If you would like to add any extended function, please do pull request to this repository