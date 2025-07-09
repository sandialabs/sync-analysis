# Locust Load Testing for Synchronic Web Ledger

This directory contains a Locust load testing script for testing the synchronic web ledger service.

## Prerequisites

1. Follow the instructions in the ledger journal service to spin up a ledger compose network: `https://github.com/sandialabs/sync-services/tree/main/compose/ledger`

2. Ensure you have the `SECRET` environment variable set (must match the server's secret)

## Running Tests

### Interactive Web UI Mode (Recommended for Development)

```bash
$ SECRET=pass locust --host=http://localhost:8192/.interface
```

**Expected Behavior:**
1. Locust starts and displays: `Starting web interface at http://localhost:8089`
2. Open your browser to http://localhost:8089
3. You'll see the Locust web interface with:
   - **Host**: Pre-filled with `http://localhost:8192/.interface`
   - **Number of users**: Input field for concurrent users
   - **Spawn rate**: Input field for users spawned per second
4. Enter desired values (e.g., 10 users, 2 spawn rate) and click **"Start swarming"**
5. Monitor real-time statistics including:
   - Requests per second
   - Response times
   - Success/failure rates
   - Individual request logs in the terminal

### Headless Mode (For Automated Testing)

```bash
$ SECRET=pass locust --host=http://localhost:8192/.interface --users=10 --spawn-rate=2 --run-time=60s --headless
```

**Expected Behavior:**
1. Test starts immediately without web interface
2. Runs for specified duration (60 seconds in example)
3. Outputs statistics to terminal
4. Exits automatically when complete

### Additional Options

```bash
# Save results to CSV files
$ SECRET=pass locust --host=http://localhost:8192/.interface --users=10 --spawn-rate=2 --run-time=60s --headless --csv=results

# Run with custom web UI port
$ SECRET=pass locust --host=http://localhost:8192/.interface --web-port=8090
```

## Test Behavior

The load test performs the following actions:
- Generates random key-value pairs
- Sends POST requests to `/.interface` endpoint with Lisp-style commands
- Each request format: `(*local* "SECRET" (ledger-set! (*state* locust KEY) VALUE))`
- Logs both request and response (truncated to 80 characters each)

## Expected Output

In the terminal, you'll see output like:
```
REQ: (*local* "pass" (ledger-set! (*state* locust key-123456) val-789012)) | RESP: #t
REQ: (*local* "pass" (ledger-set! (*state* locust key-234567) val-890123)) | RESP: #t
```

## Troubleshooting

- **Connection errors**: Ensure the ledger server is running and accessible
- **Authentication errors**: Verify the `SECRET` environment variable matches the server configuration
- **Web UI not accessible**: Check that port 8089 (or custom port) is not in use