# Zap-Automation

A really simple ZAP automator using Docker Compose to keep things self-contained and semi-stateless (just run and output).

Idea is to read a CSV of headers _target_, _whether to spider_ (`true` or `false`), and _scan type_ (`passive` or `passive_and_active`) and then use ZAP accordingly.

CSV format:

```csv
https://www.example.com,true,passive
https://example.org,false,passive_and_active
```

There should be no headers in the CSV file.

Outputs to `scanner_output/`.
