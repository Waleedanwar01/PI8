import os

# Gunicorn configuration file
# https://docs.gunicorn.org/en/stable/configure.html#configuration-file

# Bind to the port defined by the PORT environment variable, or default to 10000 (Render's default)
port = os.environ.get("PORT", "10000")
bind = f"0.0.0.0:{port}"

# Worker processes
# A general rule of thumb is (2 x num_cores) + 1
# On Render's starter tier, 2-4 workers is usually appropriate
workers = 2

# Threads per worker
# threads = 4

# Timeout
# Increase timeout for long-running requests if needed
timeout = 120

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
