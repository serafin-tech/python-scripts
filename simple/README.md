# Simple scripts

main assumptions:

- one script - one task
- standard library mostly, in case other modules are needed - modules to be installed from standard Ubuntu repository (latest LTS version)

Scripts:

1. [`cloudskillboost_profile_reader.py`](cloudskillboost_profile_reader.py) - read and process Cloud Skill Boost profile, output to Markdown table
2. [`csv2md.py`](csv2md.py) - read CSV file and convert it to Markdown table, prepared for manipulating gcloud output
3. [`csv2xlsx.py`](csv2xlsx.py) - read multiple CSV files and combine them into a single Excel file
4. [`gcp_get_api_addresses.py`](gcp_get_api_addresses.py) - get and process Google Cloud Platform API addresses to import them to router
5. [`github_get_user_keys.py`](github_get_user_keys.py) - get and process GitHub user keys to import them to router
6. [`log-loader.py`](log-loader.py) - provides functionality to forward log entries from a specified log file to a syslog server
7. [`rdap_get_domain_details.py`](rdap_get_domain_details.py) - reads domain details from RDAP database
8. [`skelton.py`](skelton.py) - skelton script to speed-up development
9. [`uptimerobot_get_probe_addresses.py`](uptimerobot_get_probe_addresses.py) - get and process UptimeRobot probe addresses to import them to router
