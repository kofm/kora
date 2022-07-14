# Installing

You will need `docker` and `docker-compose`.

```bash
git clone https://github.com/kofm/persefone
cd persefone
docker-compose up -d
docker exec -i persefone-db-1 /bin/bash -c "PGPASSWORD=postgres psql --username postgres postgres" < initial_data.sql
http://localhost:8000
```
