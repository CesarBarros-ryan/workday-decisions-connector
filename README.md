# workday-decisions-connector

Local repository for the Workday -> Decisions connector. Contains scripts to search Workday documents, build import payloads, and post them back to Workday. 

This repo was initialized locally by an assistant. 

See `main.py` for the main workflow.

VS Code Debugging notes:
- The VS Code `launch.json` in this repo points `envFile` to `${workspaceFolder}/.env`.
- If you see a popup saying "Failed to resolve env \"...python.exe\"" it usually means a launch config `env` or `envFile` entry was set incorrectly (for example, the interpreter path was pasted into `envFile` or an `env` value contains the entire python path).
- Keep `envFile` as a path (no extra quotes) and do not place the python executable path into `env` or `envFile`.
