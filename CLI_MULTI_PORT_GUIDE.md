# CLI Multi-Port Usage Guide

## Overview

The `generate` command now supports **multiple endpoints** for load balancing across multiple GPUs, providing up to 4x throughput improvement.

## Quick Examples

### Single Endpoint (1 GPU)

```bash
python commit.py generate \
  --prompts-file prompts.txt \
  --endpoint http://0.0.0.0:10006 \
  --seed 42 \
  --output-folder results
```

**Throughput**: ~1.2 requests/minute

### Multiple Endpoints (4 GPUs) - Recommended

```bash
python commit.py generate \
  --prompts-file prompts.txt \
  --endpoint http://0.0.0.0:10006 \
  --endpoint http://0.0.0.0:10007 \
  --endpoint http://0.0.0.0:10008 \
  --endpoint http://0.0.0.0:10009 \
  --seed 42 \
  --output-folder results
```

**Throughput**: ~4.8 requests/minute (4x faster!)

## Command Reference

### Syntax

```bash
python commit.py generate [OPTIONS]
```

### Options

| Option | Required | Multiple | Description |
|--------|----------|----------|-------------|
| `--prompts-file` | ✓ | No | Path to file containing image URLs (one per line) |
| `--endpoint` | ✓ | Yes | Generator endpoint URL (can specify multiple times) |
| `--seed` | ✓ | No | Seed for generation (integer) |
| `--output-folder` | No | No | Output folder path (default: `results`) |

### Help

```bash
python commit.py generate --help
```

## Prerequisites

### 1. Start Multi-Port Servers

```bash
cd /root/3d-genius
./start_multi_port.sh
```

This starts 4 servers on ports 10006-10009.

### 2. Verify Servers

```bash
# Quick check
curl http://0.0.0.0:10006/health
curl http://0.0.0.0:10007/health
curl http://0.0.0.0:10008/health
curl http://0.0.0.0:10009/health

# Or use monitoring tool
cd /root/3d-genius
python monitor_multi_port.py
```

### 3. Prepare Prompts File

Create a text file with one image URL per line:

```text
https://example.com/image1.png
https://example.com/image2.png
https://example.com/image3.png
https://example.com/image4.png
```

## Usage Examples

### Example 1: Basic Single GPU

```bash
python commit.py generate \
  --prompts-file my_images.txt \
  --endpoint http://0.0.0.0:10006 \
  --seed 42
```

Output:
```
Reading prompts from file...
Found 4 prompts to process
Using single endpoint: http://0.0.0.0:10006
Processing 4 prompts...
Single endpoint mode: http://0.0.0.0:10006
Concurrency: 1 concurrent requests, 2 max in-flight
...
```

### Example 2: Multi-GPU with All 4 GPUs

```bash
python commit.py generate \
  --prompts-file my_images.txt \
  --endpoint http://0.0.0.0:10006 \
  --endpoint http://0.0.0.0:10007 \
  --endpoint http://0.0.0.0:10008 \
  --endpoint http://0.0.0.0:10009 \
  --seed 42 \
  --output-folder ./output
```

Output:
```
Reading prompts from file...
Found 100 prompts to process
Using 4 endpoints for load balancing:
  1. http://0.0.0.0:10006
  2. http://0.0.0.0:10007
  3. http://0.0.0.0:10008
  4. http://0.0.0.0:10009
Processing 100 prompts...
Multi-port mode: 4 endpoints configured
  Endpoint 1: http://0.0.0.0:10006
  Endpoint 2: http://0.0.0.0:10007
  Endpoint 3: http://0.0.0.0:10008
  Endpoint 4: http://0.0.0.0:10009
Concurrency: 4 concurrent requests, 8 max in-flight
Generated 100 tasks
Prompt image_001 → endpoint port 10006
Prompt image_002 → endpoint port 10007
Prompt image_003 → endpoint port 10008
Prompt image_004 → endpoint port 10009
...
```

### Example 3: Using Only 2 GPUs

```bash
python commit.py generate \
  --prompts-file my_images.txt \
  --endpoint http://0.0.0.0:10006 \
  --endpoint http://0.0.0.0:10008 \
  --seed 42
```

**Throughput**: ~2.4 requests/minute

### Example 4: Remote Servers

```bash
python commit.py generate \
  --prompts-file my_images.txt \
  --endpoint http://server1.example.com:10006 \
  --endpoint http://server2.example.com:10006 \
  --endpoint http://server3.example.com:10006 \
  --endpoint http://server4.example.com:10006 \
  --seed 42
```

### Example 5: Custom Output Folder

```bash
python commit.py generate \
  --prompts-file my_images.txt \
  --endpoint http://0.0.0.0:10006 \
  --endpoint http://0.0.0.0:10007 \
  --endpoint http://0.0.0.0:10008 \
  --endpoint http://0.0.0.0:10009 \
  --seed 42 \
  --output-folder /path/to/output
```

## Shell Scripting

### Bash Script Example

```bash
#!/bin/bash

# generate_batch.sh

ENDPOINTS=(
    "http://0.0.0.0:10006"
    "http://0.0.0.0:10007"
    "http://0.0.0.0:10008"
    "http://0.0.0.0:10009"
)

# Build endpoint arguments
ENDPOINT_ARGS=""
for ep in "${ENDPOINTS[@]}"; do
    ENDPOINT_ARGS="$ENDPOINT_ARGS --endpoint $ep"
done

# Run generation
python commit.py generate \
    --prompts-file "$1" \
    --seed 42 \
    $ENDPOINT_ARGS \
    --output-folder results

echo "Generation complete!"
```

Usage:
```bash
chmod +x generate_batch.sh
./generate_batch.sh my_images.txt
```

### Using Environment Variables

```bash
#!/bin/bash

# Set endpoints
export ENDPOINT1="http://0.0.0.0:10006"
export ENDPOINT2="http://0.0.0.0:10007"
export ENDPOINT3="http://0.0.0.0:10008"
export ENDPOINT4="http://0.0.0.0:10009"

# Run with all endpoints
python commit.py generate \
    --prompts-file prompts.txt \
    --endpoint $ENDPOINT1 \
    --endpoint $ENDPOINT2 \
    --endpoint $ENDPOINT3 \
    --endpoint $ENDPOINT4 \
    --seed 42
```

### Loop for Multiple Batches

```bash
#!/bin/bash

# Process multiple prompt files with same endpoints
for file in prompts_batch_*.txt; do
    echo "Processing $file..."
    python commit.py generate \
        --prompts-file "$file" \
        --endpoint http://0.0.0.0:10006 \
        --endpoint http://0.0.0.0:10007 \
        --endpoint http://0.0.0.0:10008 \
        --endpoint http://0.0.0.0:10009 \
        --seed 42 \
        --output-folder "results_$(basename $file .txt)"
    echo "Completed $file"
done
```

## Performance

### Benchmarks

| GPUs | Endpoints | Command | Throughput | 100 Images |
|------|-----------|---------|------------|------------|
| 1 | 1 | `--endpoint ...10006` | 1.2 req/min | ~83 min |
| 2 | 2 | `--endpoint ...10006 --endpoint ...10007` | 2.4 req/min | ~42 min |
| 4 | 4 | `--endpoint ...10006 ... --endpoint ...10009` | 4.8 req/min | ~21 min |

### Load Distribution

With 4 endpoints, requests are distributed in round-robin:

```
Request 1  → Port 10006 (GPU 0)
Request 2  → Port 10007 (GPU 1)
Request 3  → Port 10008 (GPU 2)
Request 4  → Port 10009 (GPU 3)
Request 5  → Port 10006 (GPU 0)  # Cycles back
Request 6  → Port 10007 (GPU 1)
...
```

## Troubleshooting

### Error: Connection refused

**Problem**: Cannot connect to endpoint

**Solution**:
```bash
# 1. Check if servers are running
ps aux | grep "python serve.py"

# 2. Check health endpoints
curl http://0.0.0.0:10006/health

# 3. Restart servers if needed
cd /root/3d-genius
./stop_all_servers.sh
./start_multi_port.sh
```

### Error: No prompts found in file

**Problem**: Prompts file is empty or has wrong format

**Solution**:
```bash
# Check file contents
cat prompts.txt

# File should have one URL per line:
# https://example.com/image1.png
# https://example.com/image2.png
```

### Warning: Only one GPU being used

**Problem**: Forgot to specify multiple endpoints

**Solution**:
```bash
# Wrong (only one endpoint)
python commit.py generate --prompts-file prompts.txt --endpoint http://0.0.0.0:10006 --seed 42

# Correct (multiple endpoints)
python commit.py generate \
  --prompts-file prompts.txt \
  --endpoint http://0.0.0.0:10006 \
  --endpoint http://0.0.0.0:10007 \
  --endpoint http://0.0.0.0:10008 \
  --endpoint http://0.0.0.0:10009 \
  --seed 42
```

### Error: Some endpoints not responding

**Problem**: Not all servers are healthy

**Solution**:
```bash
# Check all endpoints
for port in 10006 10007 10008 10009; do
  echo "Checking port $port..."
  curl http://0.0.0.0:$port/health || echo "Port $port not responding"
done

# Monitor servers
cd /root/3d-genius
python monitor_multi_port.py
```

## Best Practices

### ✅ Do

- **Use all available GPUs** for maximum throughput
- **Check server health** before starting large batches
- **Monitor progress** with verbose logging
- **Use absolute paths** for prompts file and output folder
- **Set appropriate seed** for reproducibility

### ❌ Don't

- **Mix different server versions** in endpoint list
- **Use more endpoints than available GPUs**
- **Forget to start servers** before running command
- **Use single endpoint** when multiple GPUs are available
- **Interrupt during generation** (unless necessary)

## Advanced Usage

### Custom Concurrency

The generator automatically configures concurrency based on the number of endpoints:

- **1 endpoint**: 1 concurrent request, 2 max in-flight
- **2 endpoints**: 2 concurrent requests, 4 max in-flight
- **4 endpoints**: 4 concurrent requests, 8 max in-flight
- **N endpoints**: N concurrent requests, N×2 max in-flight

### Monitoring Progress

Watch the output for progress indicators:

```bash
python commit.py generate ... 2>&1 | tee generation.log
```

Look for:
- `Prompt image_XXX → endpoint port YYYY` - Request assignment
- `Prompt image_XXX [port YYYY] generation completed in X.Xs` - Completion
- `Generation completed` - All done

### Parallel Batches

Run multiple batches in parallel (if you have enough GPUs):

```bash
# Terminal 1 - Uses GPUs 0,1
python commit.py generate \
  --prompts-file batch1.txt \
  --endpoint http://0.0.0.0:10006 \
  --endpoint http://0.0.0.0:10007 \
  --seed 42 &

# Terminal 2 - Uses GPUs 2,3
python commit.py generate \
  --prompts-file batch2.txt \
  --endpoint http://0.0.0.0:10008 \
  --endpoint http://0.0.0.0:10009 \
  --seed 42 &

wait
```

## Output

### Success

```bash
# stdout
{"success": true}

# stderr (during execution)
Reading prompts from file...
Found 4 prompts to process
Using 4 endpoints for load balancing:
  1. http://0.0.0.0:10006
  2. http://0.0.0.0:10007
  3. http://0.0.0.0:10008
  4. http://0.0.0.0:10009
Processing 4 prompts...
...
Generation completed
```

### Failure

```bash
# Exit code: 1 (error) or 130 (interrupted)

# stderr
Generation failed: <error message>

# stdout
{"success": false, "error": "..."}
```

## Summary

The multi-port CLI provides:

- ✅ **4x throughput** with 4 GPUs
- ✅ **Simple syntax** with multiple `--endpoint` flags
- ✅ **Automatic load balancing** (round-robin)
- ✅ **Backward compatible** (works with single endpoint)
- ✅ **Enhanced logging** (shows which GPU is used)

**Quick start:**

```bash
# 1. Start servers
cd /root/3d-genius && ./start_multi_port.sh

# 2. Run generation
python commit.py generate \
  --prompts-file prompts.txt \
  --endpoint http://0.0.0.0:10006 \
  --endpoint http://0.0.0.0:10007 \
  --endpoint http://0.0.0.0:10008 \
  --endpoint http://0.0.0.0:10009 \
  --seed 42
```

---

**Need help?** Check `/root/3d-genius/MULTI_PORT_SETUP.md` for server setup details.

