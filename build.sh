#!/usr/bin/env bash
# exit on error
set -o errexit

# Build Tailwind CSS
cd theme/static_src
npm install
npm run build
cd ../..

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
