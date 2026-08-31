# VN Equity Backtest

A compact Railway-ready workspace for researching **long-only Vietnamese equity
strategies** and reviewing future TradingView signals. It contains no portfolio
tracking, derivatives, DCA, Kelly, dividend, or short-selling module.

## What it does

- Runs one or more Vietnamese stock tickers with daily OHLCV data from Vnstock.
- Executes MA crossover, RSI mean reversion, and Donchian breakout strategies.
- Uses close-of-day signals and next-session-open fills.
- Applies board-lot rounding, commission, sell tax, slippage, and a volume cap.
- Stores every run, trade, equity curve, and downloaded price bar in SQLite.
- Receives TradingView webhooks and applies ticker/action/strategy allow lists.
- Lets the dashboard classify a signal as accepted, excluded, entry, exit, watch,
  or research; it can also hard-delete an irrelevant record.
- Imports a locally executed backtest through a token-protected API and can mark
  it as the standard for that strategy.

The engine allows `BUY` and `SELL` to close an existing holding only; it never
opens a short stock position.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` and sign in with the values in `.env`. Change the
example password before exposing the app to another network.

## Deploy to Railway

1. Push this folder to a new GitHub repository.
2. In Railway, choose **New Project → Deploy from GitHub Repo**.
3. Attach a single Railway Volume at `/data`.
4. Set these Railway Variables:

```text
DATABASE_PATH=/data/backtests.db
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<strong-unique-password>
SESSION_DAYS=30
WEBHOOK_SECRET=<long-random-secret>
REQUIRE_WEBHOOK_SECRET=true
BACKTEST_UPLOAD_TOKEN=<separate-long-random-token>
```

5. Deploy. Railway uses the provided Dockerfile, `$PORT` command, and `/health`
   health check from `railway.json`.

SQLite is appropriate for one Railway service replica with its attached Volume.
Do not scale the web service horizontally without moving runs and persistence to
a shared database plus a dedicated job queue.

## TradingView webhook monitoring

Create a TradingView alert with webhook URL:

```text
https://your-railway-domain/webhook
```

Use a JSON body such as:

```json
{
  "ticker": "{{ticker}}",
  "action": "buy",
  "price": "{{close}}",
  "timeframe": "{{interval}}",
  "strategy": "MA crossover",
  "time": "{{time}}",
  "secret": "same-value-as-WEBHOOK_SECRET"
}
```

In **Điều kiện nhận tín hiệu**, set optional comma-separated ticker and strategy
allow lists plus the permitted actions. A valid signal is stored as `pending` so
you can classify it in **Signal Monitor**. A signal outside the conditions is
stored as `excluded` with its reason, giving you an audit trail without putting
it in the active review set. Only long-only `buy` and `sell` actions are
accepted; short-related actions are excluded.

## Run backtest locally and publish the standard

The local project in this workspace writes `metrics.json`, `equity_curve.csv`,
`trades.csv`, and `config.json` whenever you run a backtest. Set the same
`BACKTEST_UPLOAD_TOKEN` locally and in Railway, then publish a completed report:

```powershell
$env:BACKTEST_UPLOAD_TOKEN = "same-value-as-Railway"
python -m vn_equity_backtest publish `
  --results-dir results\my-run `
  --symbols FPT,VCB `
  --dashboard-url https://your-railway-domain `
  --set-standard
```

The result appears with source `local_import`. Marking it as a standard applies
one standard per strategy; incoming signals for that strategy show its return
and maximum drawdown in Signal Monitor. The upload token works only for the
import endpoint—do not use your administrator password in local scripts.

## Add a strategy

Strategies live in `app/services/backtesting.py`. Add a `StrategySpec` to the
`STRATEGIES` registry. Its generator receives a normalized OHLCV DataFrame and
must return a Boolean series: `True` means hold a long position, `False` means
stay flat. The API and selector discover the registry automatically. When a
strategy needs new parameters, add them to `BacktestConfig`,
`BacktestRunPayload`, and the single form in `app/static/index.html`.

## Research limitations

Vnstock data is cached for repeatability and to reduce provider requests, but
it is still a research data source. Confirm corporate-action treatment,
delisted tickers, historical index membership, trading limits, data quality,
and your broker's actual fee schedule before taking an investment decision.
