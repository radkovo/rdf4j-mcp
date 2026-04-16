#! /bin/bash
source .venv/bin/activate
cd src
FASTMCP_HOST=0.0.0.0 FASTMCP_PORT=9000 python server.py
deactivate
