## Enhanced Docker Run Command

```bash
docker run \
  --name marimo-notebook \
  --hostname marimo-dev \
  -p 18080:8080 \
  --restart unless-stopped \
  -v marimo-data:/app/data \
  -e MARIMO_SKIP_UPDATE_CHECK=1 \
  -it my_app
```

## Parameter Breakdown

### Parameter Breakdown

#### Production

| Parameter                          | Purpose                                         |
|------------------------------------|-------------------------------------------------|
| `--name marimo-notebook`           | Easy container identification and management    |
| `--hostname marimo-dev`            | Sets internal hostname for the container        |
| `-p 18080:8080`                    | Port mapping (host:container)                   |
| `--restart unless-stopped`         | Auto-restart container on system reboot         |
| `-v marimo-data:/app/data`         | Persistent storage for notebooks                |
| `-e MARIMO_SKIP_UPDATE_CHECK=1`    | Skip version check on startup                   |
| `-it`                              | Interactive terminal mode                       |

#### Development

| Parameter                                   | Purpose                                         |
|----------------------------------------------|-------------------------------------------------|
| `-v "$(pwd)/notebooks:/app/notebooks"`       | Mounts local notebooks folder for development   |
| `-v marimo-data:/app/data`                   | Persistent storage for notebooks                |
| (All other parameters as above)              | See production table for details                |

## Useful Management Commands

```bash
# Start/stop the named container
docker start marimo-notebook
docker stop marimo-notebook

# View logs
docker logs marimo-notebook

# Remove container (keeps volume)
docker rm marimo-notebook

# List volumes
docker volume ls
```

## For Development (with local file mounting)

| Parameter                                   | Purpose                                         |
|----------------------------------------------|-------------------------------------------------|
| `-v "$(pwd)/notebooks:/app/notebooks"`       | Mounts local notebooks folder for development   |

```bash
docker run \
  --name marimo-notebook \
  --hostname marimo-dev \
  -p 18080:8080 \
  --restart unless-stopped \
  -v "$(pwd)/notebooks:/app/notebooks" \
  -v marimo-data:/app/data \
  -e MARIMO_SKIP_UPDATE_CHECK=1 \
  -it my_app
```

This mounts your local `notebooks` folder so changes persist on your host system.