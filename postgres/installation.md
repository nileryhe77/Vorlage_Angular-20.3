# postgre

## Step 1 — Installing PostgreSQL
```
sudo apt update
sudo apt install postgresql postgresql-contrib
```

## Step 2 — Using PostgreSQL Roles and Databases
```
sudo systemctl start postgresql.service
sudo -u postgres createuser --interactive
```
schatzbuch
y
```
sudo -u postgres createdb schatzbuch
```

```
sudo adduser schatzbuch
```

pw: 1234_pw_#+

```
sudo -u schatzbuch psql
```

in psql:
ALTER USER schatzbuch WITH PASSWORD '#####';

### Step 3 - set up data base
```

from dataconnections import postgres as pg