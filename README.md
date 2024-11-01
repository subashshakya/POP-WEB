# POP WEB

## Run using docker compose

```docker compose up --build```

## Stoping containers and removing the volumes

```docker compose down -v```

## Run migrations using

```docker compose run web python3 /app/pop_web/manage.py makemigrations```

```docker compose run web python3 /app/pop_web/manage.py migrate```
