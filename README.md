# ChaiLedger

A transparent weighing and payment record for smallholder tea farmers in Kenya.

## African Context

In Kenya, smallholder tea farmers pick green leaf and carry it to a buying centre. A clerk weighs each sack, writes down the number, and at the end of the month the factory pays the farmer per kilogram. Everything the farmer earns depends on that one reading on the scale. Most farmers have no record of their own to check it against.

This is not just a guess. The Tea Board of Kenya has received complaints about tampered weighing scales from farmers in almost all 20 tea-growing counties. When it inspected buying centres in Bomet County, it found farmers losing between 0.5 and 1 kg on every sack of green leaf ([Food Business MEA, 2023](https://www.foodbusinessmea.com/?p=2087456)). Factories, including those managed by the Kenya Tea Development Agency (KTDA), have since added anti-tampering technology to their scales ([Food Business MEA](https://www.foodbusinessmea.com/?p=2125763)). Even so, the farmer still has no simple way to check a reading, agree with it, or question it.

I grew up close to this. During my last holiday of primary school, I went with my mum to the tea farm and helped her pick until she reached the number of kilograms she needed to get paid. Every kilogram mattered, and losing even one to a wrong reading would have meant more hours in the field.

ChaiLedger gives every farmer their own record of every weighing. The farmer either confirms each delivery or disputes it, so a wrong reading is caught on the same day instead of being discovered on payday. Over time, the disputes also show which clerks or buying centres keep having problems.

ChaiLedger is an independent student project. It is not affiliated with KTDA or the Tea Board of Kenya.

## Team Members

* Irene Winnie - Application and Documentation Lead - i.winnie@alustudent.com
* Effiong Uyo - Team Lead and Repo/DevOps Lead - e.uyo@alustudent.com

## Project Overview

ChaiLedger is a REST API that keeps track of green leaf deliveries at tea buying centres. When a clerk records a weighing, the farmer gets an SMS receipt with the weight, the centre, the clerk's name, the time and a reference number. For now the SMS is simulated, so the messages are saved in an outbox we can look at instead of being sent to real phones.

Once the receipt arrives, the farmer can confirm the weight or dispute it by giving the weight they expected and a reason. Only confirmed kilograms count towards the farmer's estimated pay for the month. Disputed kilograms are put on hold until someone reviews them. A dispute report then groups all disputes by clerk and buying centre, so a cooperative or factory officer can quickly see where a scale or a clerk needs attention.

We split the code into four modules: farmers, deliveries, payments and notifications. Each one has its own business logic and its own endpoints. This keeps things tidy now, and it means any of them could become its own service later without rewriting the others.

## Target Users

* **Smallholder tea farmers**, who receive receipts, confirm or dispute weighings, and check what they should be paid each month.
* **Buying centre clerks**, who register farmers and record each weighing at the scale.
* **Cooperative or factory officers**, who review disputes and look out for clerks or centres with too many of them.

## Core Features

* **Feature 1: Farmer and centre registration.** Register buying centres and farmers. Each farmer gets a farmer number like `CL-0001`, and phone numbers are saved in the same `+254` format however they are typed in.
* **Feature 2: Recording deliveries.** Record each weighing with the farmer, centre, kilograms, clerk and time. Weights that are zero, negative or too large for one sack are rejected.
* **Feature 3: Confirm or dispute.** Every weighing starts as `pending`. The farmer confirms it, or disputes it with their own weight and a reason. Once a weighing is confirmed or disputed, it cannot be changed again.
* **Feature 4: Monthly statement and payout estimate.** Shows the confirmed, pending and disputed kilograms for a month, and works out the estimated pay from confirmed kilograms only.
* **Feature 5: SMS receipts and dispute report.** Every weighing and every dispute sends a simulated SMS. The dispute report ranks clerks and centres by how many disputes they have and how many kilograms are in question.

## Technology Stack

* **Backend:** Python 3.10 or newer, with Flask for the REST API
* **Frontend:** None yet. The API returns JSON, which you can try with a browser, curl or Postman
* **Database:** SQLite, which saves to a local file and needs no setup
* **Testing:** pytest
* **Linting:** flake8
* **Containers:** Docker and Docker Compose. Inside the container, gunicorn serves the app instead of Flask's development server
* **CI:** GitHub Actions, which lints, tests and builds the Docker image on every push and pull request
* **Other:** python-dotenv, for reading settings from a `.env` file

## Getting Started

There are two ways to run ChaiLedger. The easiest is Docker Compose. You only need Docker installed, and one command starts everything. The Python setup is still here for when you want to change the code and run the tests yourself.

### Running with Docker Compose

#### What you need

* Docker Desktop on Windows or macOS, or Docker Engine with the Compose plugin on Linux. Check with `docker compose version`. You need version 2.24 or newer.
* Git

On Windows, open Docker Desktop and wait until it says "Engine running" before you type any Docker command. I learned this the hard way. If you skip it, you get a long error about a pipe that cannot be found.

#### Start the app

```bash
git clone https://github.com/chailedger-team/chailedger.git
cd chailedger
docker compose up -d --build
```

The first build takes a minute or two. After that, Docker reuses what it already built, so it is much quicker. Open http://localhost:5000/health in your browser. If you see `{"status":"ok"}`, everything is working, and all the curl examples in [Usage](#usage) work exactly the same.

You do not need a `.env` file. Compose already has defaults that work, and if you do create one (see step 4 under Installation), it picks up your values.

#### Everyday commands

| What you want to do | Command |
|---|---|
| Start the app | `docker compose up -d --build` |
| Load the sample centres and farmers | `docker compose --profile seed run --rm seed` |
| Check that the app is healthy | `docker compose ps` and look for `healthy` |
| Watch the logs | `docker compose logs -f app` |
| Stop the app and keep your data | `docker compose down` |
| Stop the app and delete all data | `docker compose down -v` |
| Use another port, for example 8080 | Add `APP_PORT=8080` to your `.env` file, then start the app |

#### How it works

**Dockerfile.** The image is built in two stages. The first stage installs the Python packages. The second stage starts again from a fresh `python:3.12-slim` image and only copies in those packages and our code, so nothing extra comes along. The app runs as its own user called `chailedger`, not as root, so even if something went wrong inside the app, it could not take over the container. Docker also calls `/health` every 30 seconds and marks the container as unhealthy if the app stops answering.

**docker-compose.yml.** This runs the app on its own private network and restarts it if it crashes. ChaiLedger uses SQLite, which keeps everything in one file, so there is no separate database container. Instead, that file lives in a volume called `chailedger-data`. A volume is storage that Docker keeps outside the container, so the farmers and weighings you record are still there after you stop, restart or rebuild the app. The `seed` service only runs when you ask for it, and it waits until the app is healthy before adding the sample data.

**.dockerignore.** This keeps things like `.env`, local databases, the tests and the Git history out of the image. Builds are faster, and no secrets end up inside it.

### Running with Python

#### Prerequisites

* Python 3.10 or newer (check with `python --version`)
* pip
* Git
* curl or Postman, if you want to try the API from the command line

#### Installation

1. Clone the repository

   ```bash
   git clone https://github.com/chailedger-team/chailedger.git
   cd chailedger
   ```

2. Create and activate a virtual environment

   Windows (Command Prompt):

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

   macOS or Linux:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   Your prompt should now start with `(venv)`. Run the activate command again any time you open a new terminal.

3. Install the dependencies

   ```bash
   pip install -r requirements-dev.txt
   ```

   `requirements.txt` has only what the app needs to run, and it is what the Docker image installs. `requirements-dev.txt` adds pytest and flake8 on top, so you can test and lint on your machine.

4. Create your local settings file

   Windows:

   ```
   copy .env.example .env
   ```

   macOS or Linux:

   ```bash
   cp .env.example .env
   ```

   The default values work as they are. Please never commit your `.env` file.

5. Load some sample data (optional)

   ```bash
   flask --app run seed
   ```

   This adds two buying centres and two farmers so you have something to play with.

6. Run the application

   ```bash
   python run.py
   ```

   Open http://127.0.0.1:5000 in your browser to see all the endpoints, or http://127.0.0.1:5000/health to check that the app is running. Press `Ctrl + C` to stop it.

### Running the tests and the linter

```bash
flake8
pytest
```

flake8 checks the code style and prints nothing when everything is fine. The tests create their own temporary database, so they never touch your local data. These are the same checks our CI pipeline runs on GitHub, so if both pass on your machine, they should pass there too.

## Usage

Here is the journey of one sack of tea leaves, from the scale to the farmer's statement. The examples are written for Windows Command Prompt. On macOS or Linux, the same commands work, and you can swap the `\"` for plain `"` inside single quotes.

**1. Register a buying centre**

```
curl -X POST http://127.0.0.1:5000/centres -H "Content-Type: application/json" -d "{\"name\": \"Kiamokama Buying Centre\", \"county\": \"Kisii\"}"
```

**2. Register a farmer**

```
curl -X POST http://127.0.0.1:5000/farmers -H "Content-Type: application/json" -d "{\"name\": \"Mary Wanjiku\", \"phone\": \"0712345678\", \"centre_id\": 1}"
```

**3. The clerk records a weighing, and the farmer gets an SMS receipt**

```
curl -X POST http://127.0.0.1:5000/deliveries -H "Content-Type: application/json" -d "{\"farmer_id\": 1, \"kg\": 18.5, \"clerk\": \"Otieno\"}"
```

**4. The farmer agrees and confirms it**

```
curl -X POST http://127.0.0.1:5000/deliveries/1/confirm
```

**5. Or, for another weighing, the farmer disputes it**

```
curl -X POST http://127.0.0.1:5000/deliveries/2/dispute -H "Content-Type: application/json" -d "{\"farmer_kg\": 20, \"reason\": \"My sack weighed 20 kg at home\"}"
```

**6. The farmer checks their monthly statement**

```
curl "http://127.0.0.1:5000/farmers/1/statement?month=2026-10"
```

Part of the response looks like this:

```json
{
  "farmer_no": "CL-0001",
  "month": "2026-10",
  "kg_confirmed": 18.5,
  "kg_pending": 0.0,
  "kg_disputed": 0.0,
  "rate_per_kg": 25.0,
  "estimated_payout": 462.5,
  "currency": "KES"
}
```

The rate per kilogram is an example value that you can change in `.env`. It is not an official factory rate.

**7. An officer checks the dispute report, and anyone can look at the SMS outbox**

```
curl http://127.0.0.1:5000/reports/disputes
curl "http://127.0.0.1:5000/notifications/outbox?phone=0712345678"
```

### All endpoints

| Method | Endpoint | What it does |
|---|---|---|
| GET | `/health` | Checks that the app is running |
| POST, GET | `/centres` | Adds or lists buying centres |
| POST, GET | `/farmers` | Registers or lists farmers (filter with `?centre_id=`) |
| GET | `/farmers/<id>` | Shows one farmer |
| POST, GET | `/deliveries` | Records or lists weighings (filter with `?status=`, `?farmer_id=` or `?centre_id=`) |
| GET | `/deliveries/<id>` | Shows one weighing |
| POST | `/deliveries/<id>/confirm` | The farmer confirms a weighing |
| POST | `/deliveries/<id>/dispute` | The farmer disputes a weighing |
| GET | `/farmers/<id>/statement` | Monthly statement (choose the month with `?month=YYYY-MM`) |
| GET | `/reports/disputes` | Disputes grouped by clerk and buying centre |
| GET | `/notifications/outbox` | Simulated SMS messages (filter with `?phone=`) |

### Settings

All settings are read from environment variables. You can see them in `.env.example`.

| Variable | Default | What it controls |
|---|---|---|
| `CHAILEDGER_DATABASE` | `instance/chailedger.db` | Where the SQLite file is saved |
| `CHAILEDGER_RATE_PER_KG` | `25` | Example pay rate per kilogram, in KES |
| `CHAILEDGER_MAX_KG_PER_DELIVERY` | `150` | The largest weight allowed for one weighing |
| `HOST` | `127.0.0.1` | The address the app listens on. Docker sets this to `0.0.0.0` inside the container |
| `PORT` | `5000` | The port the app runs on |
| `FLASK_DEBUG` | `0` | Set to `1` to reload the app automatically while coding |

## Project Structure

```
chailedger/
|-- app/
|   |-- __init__.py          Creates the app and connects all the modules
|   |-- config.py            Reads settings from environment variables
|   |-- db.py                Database connection, plus the init-db and seed commands
|   |-- schema.sql           Database tables
|   |-- errors.py            Error types and JSON error messages
|   |-- validation.py        Checks for phone numbers, weights and dates
|   |-- farmers/             Farmers and buying centres
|   |   |-- routes.py
|   |   `-- service.py
|   |-- deliveries/          Weighings, confirm, dispute and the dispute report
|   |   |-- routes.py
|   |   `-- service.py
|   |-- payments/            Monthly statements and payout estimates
|   |   |-- routes.py
|   |   `-- service.py
|   `-- notifications/       The simulated SMS outbox
|       |-- routes.py
|       `-- service.py
|-- tests/                   Unit and API tests
|-- docs/                    Notes on our team process
|-- .dockerignore            Files kept out of the Docker image
|-- .env.example             Example settings, with no secrets
|-- .flake8                  Linting rules
|-- docker-compose.yml       Starts the app and its data volume with one command
|-- Dockerfile               Builds the ChaiLedger image
|-- pytest.ini
|-- requirements.txt         Packages the app needs to run
|-- requirements-dev.txt     Extra packages for testing and linting
|-- run.py                   Starts the app
`-- README.md
```

In every module, `routes.py` handles the web requests and `service.py` holds the actual logic. The modules only talk to each other through their service functions. For example, we could later swap the simulated SMS for a real SMS provider just by changing the notifications module, and nothing else would need to change.

## Links

- [Project Board](https://github.com/orgs/chailedger-team/projects/1)
- [GitHub Repository](https://github.com/chailedger-team/chailedger)
- [Team Task Spreadsheet](https://docs.google.com/spreadsheets/d/1OJ5yaELHKvDsbao7nS0HjPpASoF2m0Fbyl95jkZHtyI/edit?gid=0#gid=0)

## Branch Protection

The `main` branch is protected to keep the project stable and make sure changes are reviewed before they are merged.

- **Require a pull request before merging:** All changes must be submitted through a pull request instead of being pushed directly to `main`.
- **Require one approving review:** At least one teammate must review and approve a pull request before it can be merged.
- **Dismiss stale approvals:** If new commits are pushed after approval, the previous approval is dismissed so the updated changes can be reviewed.
- **Require branches to be up to date:** Pull requests must include the latest changes from `main` before merging, reducing integration problems.
- **Require conversation resolution:** Review comments and requested changes must be addressed before merging.
- **Do not allow bypassing the rules:** The branch protection requirements apply consistently, preventing team members from skipping the review process.

These rules support collaboration, code quality and a clear history of reviewed changes.


## License

This project uses the MIT License. See the [LICENSE](LICENSE) file for details.
