#!/bin/bash
#
set -euo pipefail
flask --app external_service.app:app run
