# goit-pythonweb-hw-06

## Setup

**1. Start PostgreSQL**

```bash
docker run --name goit-postgres -p 5432:5432 -e POSTGRES_PASSWORD=yourpassword -d postgres
```

**2. Configure environment**

```bash
cp .env.example .env
```

Edit `.env` with your credentials.

**3. Install dependencies**

```bash
uv sync
```

**4. Apply migrations**

```bash
alembic upgrade head
```

**5. Seed the database**

```bash
python seed.py
```

## CRUD CLI

```bash
python main.py -a create -m Teacher -n 'Borya Jonson'
python main.py -a list   -m Teacher
python main.py -a update -m Teacher --id 1 -n 'Andrii Bezos'
python main.py -a remove -m Teacher --id 1
```

Supported models: `Group`, `Teacher`, `Student`, `Subject`, `Grade`.
