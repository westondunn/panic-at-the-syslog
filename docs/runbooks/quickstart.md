# Panic! At The Syslog — Quick Start

Get the full Tier 1 stack running locally in 5 minutes.

## Prerequisites

- **Docker** 20.10+ with Compose v2
- **8GB RAM** minimum (16GB recommended for Ollama LLM)
- **Available ports**: 1514 (syslog), 3000 (UI), 8000 (API), 5432 (Postgres), 9092 (Kafka), 11434 (Ollama)

## Step 1: Clone and configure

```bash
git clone https://github.com/westondunn/panic-at-the-syslog.git
cd panic-at-the-syslog
```

Create your environment file:

```bash
cp .env.example .env
```

**IMPORTANT**: Edit `.env` and change `PANIC_JWT_SECRET` before starting:

```bash
# Generate a secure secret (Linux/macOS/WSL)
openssl rand -hex 32

# Or on Windows PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

Copy the output and set it in `.env`:

```bash
PANIC_JWT_SECRET=your-generated-secret-here
```

## Step 2: Start Tier 1 stack

From the repository root:

```bash
docker compose -f deploy/compose/docker-compose.tier1.yml up --build -d
```

**What's starting:**

- **Kafka** (message bus, KRaft mode - no Zookeeper needed)
- **Postgres** (event storage and API database)
- **Ollama** (local LLM for analysis - downloads ~4GB model on first run)
- **Ingress** (syslog receiver - fully functional!)
- **Normalizer** (event parser - needs consumer runner - TODO)
- **Detector** (rule-based pattern detection - needs consumer runner - TODO)
- **Analyzer** (LLM-powered insights - needs consumer runner - TODO)
- **API** (REST endpoints - fully functional!)
- **UI** (web dashboard - fully functional!)

> **Note**: Consumer services (normalizer, detector, analyzer) have placeholder commands until Kafka consumer loops are implemented. See [`deploy/docker/README.md`](../../deploy/docker/README.md) for details.

## Step 3: Verify infrastructure

Wait ~60 seconds for Ollama to download the model, then check:

```bash
# Check all containers are running
docker compose -f deploy/compose/docker-compose.tier1.yml ps

# Test Kafka
docker compose -f deploy/compose/docker-compose.tier1.yml exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --list

# Test Postgres
docker compose -f deploy/compose/docker-compose.tier1.yml exec postgres psql -U panic -d panic -c '\dt'

# Test Ollama (may take 1-2 min on first start)
curl http://localhost:11434/api/tags
```

## Step 4: Verify services are running

Check that all containers are up:

```bash
docker compose -f deploy/compose/docker-compose.tier1.yml ps

# Check ingress logs (should show syslog listener started)
docker compose -f deploy/compose/docker-compose.tier1.yml logs ingress

# Check API (should respond with JSON)
curl http://localhost:8000/healthz
```

## Step 5: Send test syslog event

Once ingress is active:

```bash
# UDP test (Linux/macOS/WSL)
echo "<14>$(date '+%b %d %H:%M:%S') test-router: Interface GigabitEthernet0/1 changed state to up" \
  | nc -u localhost 1514

# PowerShell test (Windows)
"<14>$(Get-Date -Format 'MMM dd HH:mm:ss') test-router: Interface GigabitEthernet0/1 changed state to up" |
  Out-String | %{[System.Text.Encoding]::UTF8.GetBytes($_)} |
  %{ $c = New-Object System.Net.Sockets.UdpClient; $c.Connect('localhost',1514); $c.Send($_,_.Length); $c.Close() }
```

## Step 6: Access the UI

Open [http://localhost:3000](http://localhost:3000) (once UI Dockerfile is built).

Expected flow:

1. Dashboard shows raw event count.

**Expected behavior (once consumer runners are implemented):**

1. Dashboard shows raw event count
2. Normalized event appears in event list
3. Findings tab shows detected patterns (if rules match)
4. Insights tab shows LLM recommendations (~30s delay)

**Current state:**

- UI loads successfully
- APBuild failures

```bash
# Clean build (removes cached layers)
docker compose -f deploy/compose/docker-compose.tier1.yml build --no-cache

# Check for missing dependencies
docker compose -f deploy/compose/docker-compose.tier1.yml build --progress=plain
```

### I healthcheck works

- Ingress accepts syslog messages
- **Consumer pipeline is incomplete** - normalizer/detector/analyzer need Kafka consumer loops

To complete the pipeline, see [`deploy/docker/README.md`](../../deploy/docker/README.md) for consumer implementation patterns.

## Step 7: Clean up

# Wait for healthcheck to pass

docker compose -f deploy/compose/docker-compose.tier1.yml logs kafka

# Manually create topics if auto-create fails

docker compose -f deploy/compose/docker-compose.tier1.yml exec kafka \
 kafka-topics.sh --create --topic raw.syslog.v1 --bootstrap-server localhost:9092

````

### Ollama takes forever / runs out of memory
```bash
# Check model download progress
docker compose -f deploy/compose/docker-compose.tier1.yml logs ollama

# Use a smaller model (edit .env)
PANIC_OLLAMA_MODEL=llama3:8b  # Default, ~4GB
# or
PANIC_OLLAMA_MODEL=tinyllama  # Lighter, ~1GB
````

### Syslog not arriving

- Verify UDP port 1514 is open: `netstat -an | grep 1514`
- Check Windows Firewall / iptables rules
- Use TCP instead: `nc localhost 1514` (once TCP listener is implemented)

### Postgres connection refused

```bash
# Wait for healthcheck
docker compose -f deploy/compose/docker-compose.tier1.yml logs postgres
Complete the pipeline**: Implement Kafka consumer runners for normalizer/detector/analyzer (see [`deploy/docker/README.md`](../../deploy/docker/README.md))
# Initialize schema (once migrations are added)
docker compose -f deploy/compose/docker-compose.tier1.yml exec api <migration-command>
```

## Clean up

```bash
# Stop services but keep data
docker compose -f deploy/compose/docker-compose.tier1.yml down

# Stop and wipe all data (Kafka topics, DB, models)
docker compose -f deploy/compose/docker-compose.tier1.yml down -v
```

## Next steps

- **Add real services**: Create Dockerfiles in `deploy/docker/`
- **Run tests**: `make test` (unit), `make e2e-tier1` (integration)
- **Production deployment**: See [kubernetes.md](kubernetes.md)
- **Observability**: Add Prometheus/Grafana profile (see [docker-compose.md](docker-compose.md))
- **Understand contracts**: Read [contracts.md](../contracts.md) for event schemas

## Support

- **Docs**: [docs/](../)
- **Issues**: [GitHub Issues](https://github.com/westondunn/panic-at-the-syslog/issues)
- **Security**: See [SECURITY.md](../../SECURITY.md)
