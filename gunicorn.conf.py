bind = "0.0.0.0:10000"    # Listen on all networks, port 10000
workers = 2                # Run 2 copies of your app
threads = 4                # Each copy can handle 4 requests
worker_class = "sync"      # How to handle requests
worker_connections = 1000  # Maximum connections
timeout = 120              # Wait 2 minutes before timing out