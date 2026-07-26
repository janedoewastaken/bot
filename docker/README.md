# Docker

Two ways to run the bot:

| Compose file | Image | Use when |
|---|---|---|
| `docker-compose.yml` | **Custom build** from this repo | You have local changes (e.g. Labyrinth leaderboard OCR) |
| `docker-compose.official.yml` | `ghcr.io/whiteout-project/bot:latest` | You want the stock bot with auto-updates |

## Custom build (local features)

From this `docker/` directory:

```bash
cp .env.example .env
# Edit .env — paste your DISCORD_BOT_TOKEN

docker compose build
docker compose up -d
```

The bot connects to Discord exactly like the official image. Your existing data is kept if you point `WOS_DB_PATH` at the same folder as before (default inside `docker/` is `./data/db`).

### Migrate from the official container

If you already run the official image with `/opt/docker/wos/db`:

```bash
# In .env
WOS_DB_PATH=/opt/docker/wos/db
```

Stop the old container, then build and start the custom one:

```bash
docker stop wos-discord-bot
docker compose build
docker compose up -d
```

### After changing code

```bash
docker compose build && docker compose up -d
```

`UPDATE=0` is set so restarts do **not** replace your custom code with an upstream release.

### Logs

```bash
docker compose logs -f
```

## Official image (no custom code)

```bash
cp .env.example .env
docker compose -f docker-compose.official.yml pull
docker compose -f docker-compose.official.yml up -d
```

Updates apply automatically on restart (`UPDATE=1` by default).

## Environment variables

| Variable | Custom build | Official |
|---|---|---|
| `DISCORD_BOT_TOKEN` | Required | Required |
| `WOS_DB_PATH` | Host path → `/app/db` | Same |
| `UPDATE` | `0` (fixed) | `1` default |
| `BETA` | — | Optional |
| `DEBUG` | — | Optional |
