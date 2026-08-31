from __future__ import annotations

import inspect
from dataclasses import asdict, dataclass
from math import floor
from typing import Any, Callable, Mapping

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class BacktestConfig:
    """Daily long-only assumptions for Vietnamese equity research.

    Signals are evaluated at the close and filled at the following session's
    open.  The simulator can buy or sell an owned position only; it never opens
    a short position.
    """

    initial_cash: float = 1_000_000_000.0
    strategy_name: str = "ma_crossover"
    fast_window: int = 20
    slow_window: int = 100
    rsi_window: int = 14
    rsi_entry: float = 30.0
    rsi_exit: float = 55.0
    breakout_window: int = 55
    breakout_exit_window: int = 20
    commission_rate: float = 0.0015
    sell_tax_rate: float = 0.0010
    slippage_bps: float = 10.0
    lot_size: int = 100
    max_participation_rate: float = 0.05
    rebalance_interval_days: int = 20
    annualisation_days: int = 252
    risk_free_rate: float = 0.0

    def __post_init__(self) -> None:
        if self.initial_cash <= 0:
            raise ValueError("Initial capital must be positive")
        if not 0 < self.fast_window < self.slow_window:
            raise ValueError("Fast MA must be positive and smaller than slow MA")
        if self.rsi_window <= 1 or not 0 < self.rsi_entry < self.rsi_exit < 100:
            raise ValueError("RSI settings are invalid")
        if self.breakout_window <= 1 or self.breakout_exit_window <= 1:
            raise ValueError("Donchian windows must be greater than one")
        if self.lot_size <= 0 or not 0 < self.max_participation_rate <= 1:
            raise ValueError("Lot size or volume participation setting is invalid")
        if self.rebalance_interval_days <= 0:
            raise ValueError("Rebalance interval must be positive")
        if min(self.commission_rate, self.sell_tax_rate, self.slippage_bps) < 0:
            raise ValueError("Costs cannot be negative")

    @property
    def slippage_rate(self) -> float:
        return self.slippage_bps / 10_000

    def serialisable(self) -> dict[str, Any]:
        return asdict(self)


LongSignalGenerator = Callable[[pd.DataFrame, BacktestConfig], pd.Series]


@dataclass(frozen=True)
class StrategySpec:
    key: str
    label: str
    description: str
    signal_generator: LongSignalGenerator


def _ma_crossover(frame: pd.DataFrame, config: BacktestConfig) -> pd.Series:
    fast = frame["close"].rolling(config.fast_window, min_periods=config.fast_window).mean()
    slow = frame["close"].rolling(config.slow_window, min_periods=config.slow_window).mean()
    return (fast > slow).fillna(False).astype(bool)


def _rsi_mean_reversion(frame: pd.DataFrame, config: BacktestConfig) -> pd.Series:
    delta = frame["close"].diff()
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)
    average_gain = gains.ewm(
        alpha=1 / config.rsi_window, adjust=False, min_periods=config.rsi_window
    ).mean()
    average_loss = losses.ewm(
        alpha=1 / config.rsi_window, adjust=False, min_periods=config.rsi_window
    ).mean()
    rsi = 100 - 100 / (1 + average_gain / average_loss.replace(0, float("nan")))
    rsi = rsi.mask((average_loss == 0) & (average_gain > 0), 100.0)
    rsi = rsi.mask((average_loss == 0) & (average_gain == 0), 50.0)

    targets: list[bool] = []
    holding = False
    for value in rsi:
        if pd.notna(value):
            if not holding and value <= config.rsi_entry:
                holding = True
            elif holding and value >= config.rsi_exit:
                holding = False
        targets.append(holding)
    return pd.Series(targets, index=frame.index, dtype=bool)


def _donchian_breakout(frame: pd.DataFrame, config: BacktestConfig) -> pd.Series:
    prior_high = frame["high"].rolling(
        config.breakout_window, min_periods=config.breakout_window
    ).max().shift(1)
    prior_low = frame["low"].rolling(
        config.breakout_exit_window, min_periods=config.breakout_exit_window
    ).min().shift(1)
    entries = frame["close"] > prior_high
    exits = frame["close"] < prior_low
    targets: list[bool] = []
    holding = False
    for entry, exit_ in zip(entries, exits, strict=True):
        if not holding and bool(entry):
            holding = True
        elif holding and bool(exit_):
            holding = False
        targets.append(holding)
    return pd.Series(targets, index=frame.index, dtype=bool)


STRATEGIES: dict[str, StrategySpec] = {
    "ma_crossover": StrategySpec(
        key="ma_crossover",
        label="MA crossover",
        description="Nắm giữ khi MA nhanh cao hơn MA chậm.",
        signal_generator=_ma_crossover,
    ),
    "rsi_mean_reversion": StrategySpec(
        key="rsi_mean_reversion",
        label="RSI mean reversion",
        description="Mua khi RSI quá bán và thoát khi RSI hồi về ngưỡng chốt.",
        signal_generator=_rsi_mean_reversion,
    ),
    "donchian_breakout": StrategySpec(
        key="donchian_breakout",
        label="Donchian breakout",
        description="Mua khi phá đỉnh Donchian, thoát khi thủng đáy Donchian.",
        signal_generator=_donchian_breakout,
    ),
}


def strategy_catalog() -> list[dict[str, str]]:
    return [
        {"key": spec.key, "label": spec.label, "description": spec.description}
        for spec in STRATEGIES.values()
    ]


def parse_symbols(value: str | list[str]) -> list[str]:
    candidates = value.split(",") if isinstance(value, str) else value
    symbols = [str(symbol).strip().upper() for symbol in candidates if str(symbol).strip()]
    if not symbols:
        raise ValueError("At least one ticker is required")
    if len(symbols) > 20:
        raise ValueError("A run can include at most 20 tickers")
    return list(dict.fromkeys(symbols))


def normalise_ohlcv(raw: pd.DataFrame, symbol: str) -> pd.DataFrame:
    if raw is None or raw.empty:
        raise ValueError(f"No OHLCV rows were returned for {symbol}")
    aliases = {
        "time": "date", "datetime": "date", "tradingdate": "date", "date": "date",
        "open": "open", "high": "high", "low": "low", "close": "close", "volume": "volume",
    }
    frame = raw.rename(columns={column: aliases.get(column.lower(), column) for column in raw.columns})
    required = ("date", "open", "high", "low", "close", "volume")
    missing = [column for column in required if column not in frame]
    if missing:
        raise ValueError(f"{symbol} data is missing: {', '.join(missing)}")
    frame = frame.loc[:, required].copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    if getattr(frame["date"].dt, "tz", None) is not None:
        frame["date"] = frame["date"].dt.tz_convert("Asia/Ho_Chi_Minh").dt.tz_localize(None)
    for column in ("open", "high", "low", "close", "volume"):
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame["symbol"] = symbol.upper()
    frame = frame.dropna().drop_duplicates("date").sort_values("date").reset_index(drop=True)
    invalid = (frame[["open", "high", "low", "close"]] <= 0).any(axis=1) | (frame["volume"] < 0)
    if invalid.any():
        raise ValueError(f"{symbol} includes invalid OHLCV values")
    return frame.loc[:, ["date", "symbol", "open", "high", "low", "close", "volume"]]


def download_vnstock_ohlcv(symbol: str, start: str, end: str) -> pd.DataFrame:
    """Fetch complete daily bars from Vnstock's current Unified API."""
    try:
        from vnstock import Market
    except ImportError as error:  # pragma: no cover - deployment dependency
        raise RuntimeError("Vnstock is not installed") from error

    market = Market()
    equity = market.equity
    if callable(equity):
        ohlcv = equity(symbol.upper()).ohlcv
        parameters = inspect.signature(ohlcv).parameters
        interval_key = "resolution" if "resolution" in parameters else "interval"
        raw = ohlcv(start=start, end=end, count=10_000, **{interval_key: "1D"})
    else:  # Compatibility with earlier Vnstock releases.
        raw = equity.ohlcv(symbol=symbol.upper(), start=start, end=end, interval="1D")
    return normalise_ohlcv(raw, symbol)


@dataclass
class BacktestResult:
    equity_curve: pd.DataFrame
    trades: pd.DataFrame
    metrics: dict[str, float | int | str]


def _round_lot(quantity: float, lot_size: int) -> int:
    return max(0, floor(quantity / lot_size) * lot_size)


def _prepare_frames(
    data: Mapping[str, pd.DataFrame], config: BacktestConfig
) -> dict[str, pd.DataFrame]:
    strategy = STRATEGIES.get(config.strategy_name)
    if strategy is None:
        raise ValueError(f"Unknown strategy: {config.strategy_name}")
    prepared: dict[str, pd.DataFrame] = {}
    for symbol, raw in data.items():
        frame = normalise_ohlcv(raw, symbol).copy()
        # Signal at close T becomes actionable at the open of T + 1.
        frame["target_long"] = strategy.signal_generator(frame, config).shift(
            1, fill_value=False
        ).astype(bool)
        prepared[symbol] = frame.set_index("date", drop=False)
    return prepared


def _metrics(
    equity_curve: pd.DataFrame, config: BacktestConfig, trade_count: int
) -> dict[str, float | int | str]:
    values = equity_curve["equity"].astype(float)
    returns = values.pct_change().dropna()
    days = max((equity_curve["date"].iat[-1] - equity_curve["date"].iat[0]).days, 1)
    total_return = values.iat[-1] / values.iat[0] - 1
    cagr = (values.iat[-1] / values.iat[0]) ** (365.25 / days) - 1
    annual_volatility = returns.std(ddof=0) * np.sqrt(config.annualisation_days) if not returns.empty else 0.0
    excess_daily = returns - config.risk_free_rate / config.annualisation_days
    sharpe = (
        excess_daily.mean() / excess_daily.std(ddof=0) * np.sqrt(config.annualisation_days)
        if len(excess_daily) > 1 and excess_daily.std(ddof=0) > 0 else 0.0
    )
    drawdown = values / values.cummax() - 1
    return {
        "start_date": equity_curve["date"].iat[0].date().isoformat(),
        "end_date": equity_curve["date"].iat[-1].date().isoformat(),
        "starting_equity": round(float(values.iat[0]), 2),
        "ending_equity": round(float(values.iat[-1]), 2),
        "total_return": round(float(total_return), 6),
        "cagr": round(float(cagr), 6),
        "annual_volatility": round(float(annual_volatility), 6),
        "sharpe": round(float(sharpe), 4),
        "max_drawdown": round(float(drawdown.min()), 6),
        "trade_count": trade_count,
        "strategy": config.strategy_name,
    }


def run_backtest(data: Mapping[str, pd.DataFrame], config: BacktestConfig) -> BacktestResult:
    """Run equal-weight daily orders, allowing BUY and SELL-to-close only."""
    frames = _prepare_frames(data, config)
    calendar = sorted({trade_date for frame in frames.values() for trade_date in frame.index})
    if not calendar:
        raise ValueError("No price data supplied")

    cash = float(config.initial_cash)
    positions = {symbol: 0 for symbol in frames}
    last_close: dict[str, float] = {}
    trades: list[dict[str, object]] = []
    equity_rows: list[dict[str, object]] = []
    previous_active: set[str] = set()
    last_rebalance_index = -config.rebalance_interval_days

    for day_index, trade_date in enumerate(calendar):
        bars = {
            symbol: frame.loc[trade_date] if trade_date in frame.index else None
            for symbol, frame in frames.items()
        }
        executable = {
            symbol: bar for symbol, bar in bars.items()
            if bar is not None and float(bar["open"]) > 0 and float(bar["volume"]) >= 0
        }
        active = [symbol for symbol, bar in executable.items() if bool(bar["target_long"])]
        active_set = set(active)
        open_equity = cash + sum(
            quantity * float(executable[symbol]["open"] if symbol in executable else last_close.get(symbol, 0))
            for symbol, quantity in positions.items() if quantity
        )
        should_rebalance = (
            active_set != previous_active
            or day_index - last_rebalance_index >= config.rebalance_interval_days
        )
        targets = positions.copy()
        for symbol in positions:
            if symbol not in active_set:
                targets[symbol] = 0
        if should_rebalance and active:
            target_value = open_equity / len(active)
            for symbol in active:
                price = float(executable[symbol]["open"]) * (1 + config.slippage_rate)
                targets[symbol] = _round_lot(target_value / price, config.lot_size)
            last_rebalance_index = day_index
        elif should_rebalance:
            last_rebalance_index = day_index
        previous_active = active_set

        # Sells happen before buys, ensuring one cash balance for the session.
        for symbol in sorted(executable):
            current, desired = positions[symbol], targets[symbol]
            if current <= desired:
                continue
            bar = executable[symbol]
            cap = _round_lot(float(bar["volume"]) * config.max_participation_rate, config.lot_size)
            quantity = min(current - desired, cap)
            if quantity <= 0:
                continue
            fill = float(bar["open"]) * (1 - config.slippage_rate)
            notional = quantity * fill
            costs = notional * (config.commission_rate + config.sell_tax_rate)
            cash += notional - costs
            positions[symbol] -= quantity
            trades.append({"date": trade_date, "symbol": symbol, "side": "SELL", "quantity": quantity, "fill_price": fill, "notional": notional, "costs": costs})

        for symbol in sorted(active):
            current, desired = positions[symbol], targets[symbol]
            if desired <= current:
                continue
            bar = executable[symbol]
            cap = _round_lot(float(bar["volume"]) * config.max_participation_rate, config.lot_size)
            fill = float(bar["open"]) * (1 + config.slippage_rate)
            affordable = _round_lot(cash / (fill * (1 + config.commission_rate)), config.lot_size)
            quantity = min(desired - current, cap, affordable)
            if quantity <= 0:
                continue
            notional = quantity * fill
            costs = notional * config.commission_rate
            cash -= notional + costs
            positions[symbol] += quantity
            trades.append({"date": trade_date, "symbol": symbol, "side": "BUY", "quantity": quantity, "fill_price": fill, "notional": notional, "costs": costs})

        close_equity = cash
        for symbol, quantity in positions.items():
            if not quantity:
                continue
            bar = bars[symbol]
            if bar is not None:
                last_close[symbol] = float(bar["close"])
            close_equity += quantity * last_close.get(symbol, 0)
        equity_rows.append({
            "date": trade_date, "equity": close_equity, "cash": cash,
            "invested_symbols": sum(quantity > 0 for quantity in positions.values()),
        })

    equity_curve = pd.DataFrame(equity_rows)
    trade_frame = pd.DataFrame(
        trades, columns=["date", "symbol", "side", "quantity", "fill_price", "notional", "costs"]
    )
    return BacktestResult(equity_curve, trade_frame, _metrics(equity_curve, config, len(trade_frame)))
