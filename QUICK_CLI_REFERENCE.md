# Quick CLI Reference - Multi-Port Generate

## TL;DR

### Single GPU
```bash
python commit.py generate \
  --prompts-file prompts.txt \
  --endpoint http://0.0.0.0:10006 \
  --seed 42
```

### 4 GPUs (4x faster!)
```bash
python commit.py generate \
  --prompts-file prompts.txt \
  --endpoint http://0.0.0.0:10006 \
  --endpoint http://0.0.0.0:10007 \
  --endpoint http://0.0.0.0:10008 \
  --endpoint http://0.0.0.0:10009 \
  --seed 42
```

## Before You Start

```bash
# 1. Start servers
cd /root/3d-genius && ./start_multi_port.sh

# 2. Check they're running
curl http://0.0.0.0:10006/health
curl http://0.0.0.0:10007/health
curl http://0.0.0.0:10008/health
curl http://0.0.0.0:10009/health
```

## Command Syntax

```bash
python commit.py generate \
  --prompts-file <FILE> \
  --endpoint <URL> [--endpoint <URL> ...] \
  --seed <NUMBER> \
  [--output-folder <PATH>]
```

## Options

| Flag | Required | Description | Example |
|------|----------|-------------|---------|
| `--prompts-file` | ✓ | File with image URLs (one per line) | `prompts.txt` |
| `--endpoint` | ✓ | Endpoint URL (repeat for multiple) | `http://0.0.0.0:10006` |
| `--seed` | ✓ | Generation seed | `42` |
| `--output-folder` | | Output directory (default: `results`) | `./output` |

## Examples

### 1 GPU
```bash
python commit.py generate --prompts-file prompts.txt --endpoint http://0.0.0.0:10006 --seed 42
```
**Speed**: 1.2 req/min

### 2 GPUs
```bash
python commit.py generate --prompts-file prompts.txt \
  --endpoint http://0.0.0.0:10006 \
  --endpoint http://0.0.0.0:10007 \
  --seed 42
```
**Speed**: 2.4 req/min

### 4 GPUs
```bash
python commit.py generate --prompts-file prompts.txt \
  --endpoint http://0.0.0.0:10006 \
  --endpoint http://0.0.0.0:10007 \
  --endpoint http://0.0.0.0:10008 \
  --endpoint http://0.0.0.0:10009 \
  --seed 42
```
**Speed**: 4.8 req/min

### Custom Output
```bash
python commit.py generate --prompts-file prompts.txt \
  --endpoint http://0.0.0.0:10006 \
  --endpoint http://0.0.0.0:10007 \
  --endpoint http://0.0.0.0:10008 \
  --endpoint http://0.0.0.0:10009 \
  --seed 42 \
  --output-folder /path/to/output
```

## Prompts File Format

Create `prompts.txt` with one URL per line:

```text
https://example.com/image1.png
https://example.com/image2.png
https://example.com/image3.png
```

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection refused | Check servers: `curl http://0.0.0.0:10006/health` |
| Servers not running | Start: `cd /root/3d-genius && ./start_multi_port.sh` |
| Empty prompts file | Check format: `cat prompts.txt` |
| Only one GPU used | Add more `--endpoint` flags |

## Performance

| GPUs | Time for 100 images |
|------|---------------------|
| 1    | ~83 minutes        |
| 2    | ~42 minutes        |
| 4    | ~21 minutes        |

## Shell Alias (Optional)

Add to `~/.bashrc`:

```bash
alias gen4="python /root/404-cli/commit.py generate \
  --endpoint http://0.0.0.0:10006 \
  --endpoint http://0.0.0.0:10007 \
  --endpoint http://0.0.0.0:10008 \
  --endpoint http://0.0.0.0:10009"
```

Then use:
```bash
gen4 --prompts-file prompts.txt --seed 42
```

## More Help

- Full guide: `CLI_MULTI_PORT_GUIDE.md`
- Server setup: `/root/3d-genius/MULTI_PORT_SETUP.md`
- Help: `python commit.py generate --help`

