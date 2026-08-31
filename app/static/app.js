const els = {
  loginScreen: document.querySelector("#loginScreen"),
  loginForm: document.querySelector("#loginForm"),
  loginUsername: document.querySelector("#loginUsername"),
  loginPassword: document.querySelector("#loginPassword"),
  loginError: document.querySelector("#loginError"),
  appShell: document.querySelector("#appShell"),
  currentUser: document.querySelector("#currentUser"),
  logoutButton: document.querySelector("#logoutButton"),
  signalTotal: document.querySelector("#signalTotal"),
  signalPending: document.querySelector("#signalPending"),
  signalAccepted: document.querySelector("#signalAccepted"),
  signalExcluded: document.querySelector("#signalExcluded"),
  signalFiltersForm: document.querySelector("#signalFiltersForm"),
  allowedTickers: document.querySelector("#allowedTickers"),
  allowedStrategies: document.querySelector("#allowedStrategies"),
  allowBuy: document.querySelector("#allowBuy"),
  allowSell: document.querySelector("#allowSell"),
  signalStatusFilter: document.querySelector("#signalStatusFilter"),
  signalTickerFilter: document.querySelector("#signalTickerFilter"),
  refreshSignals: document.querySelector("#refreshSignals"),
  signalsTable: document.querySelector("#signalsTable"),
  form: document.querySelector("#backtestForm"),
  symbols: document.querySelector("#symbols"),
  strategy: document.querySelector("#strategy"),
  strategyDescription: document.querySelector("#strategyDescription"),
  runButton: document.querySelector("#runButton"),
  runStatus: document.querySelector("#runStatus"),
  runHistory: document.querySelector("#runHistory"),
  resultTitle: document.querySelector("#resultTitle"),
  metrics: document.querySelector("#metrics"),
  equityChart: document.querySelector("#equityChart"),
  drawdownChart: document.querySelector("#drawdownChart"),
  trades: document.querySelector("#trades"),
  localPublishCommand: document.querySelector("#localPublishCommand"),
  setStandard: document.querySelector("#setStandard"),
  downloadTrades: document.querySelector("#downloadTrades"),
  deleteRun: document.querySelector("#deleteRun"),
};

let strategies = [];
let runs = [];
let signals = [];
let activeRunId = null;
let equityChart = null;
let drawdownChart = null;
let pollTimer = null;

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;",
  }[character]));
}

function formatVnd(value) {
  return new Intl.NumberFormat("vi-VN", {
    style: "currency", currency: "VND", maximumFractionDigits: 0,
  }).format(Number(value || 0));
}

function formatPercent(value) {
  return `${(Number(value || 0) * 100).toFixed(2)}%`;
}

function setStatus(text, tone = "") {
  els.runStatus.textContent = text;
  els.runStatus.className = `statusText ${tone}`.trim();
}

async function request(url, options) {
  const response = await fetch(url, options);
  if (response.status === 401) showLogin();
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail || `${response.status} ${response.statusText}`);
  }
  return response.json();
}

function showLogin() {
  clearTimeout(pollTimer);
  els.appShell.hidden = true;
  els.loginScreen.hidden = false;
  els.loginPassword.value = "";
  els.loginUsername.focus();
}

function showApp(user) {
  els.loginScreen.hidden = true;
  els.appShell.hidden = false;
  els.currentUser.textContent = user.username;
}

async function loadStrategies() {
  const payload = await request("/api/backtests/strategies");
  strategies = payload.strategies || [];
  els.strategy.innerHTML = strategies.map((strategy) => (
    `<option value="${escapeHtml(strategy.key)}">${escapeHtml(strategy.label)}</option>`
  )).join("");
  els.strategy.value = strategies.some((item) => item.key === "ma_crossover")
    ? "ma_crossover" : strategies[0]?.key || "";
  updateStrategyForm();
}

function updateStrategyForm() {
  const selected = els.strategy.value;
  const strategy = strategies.find((item) => item.key === selected);
  els.strategyDescription.textContent = strategy?.description || "";
  document.querySelectorAll("[data-strategy-settings]").forEach((group) => {
    const visible = group.dataset.strategySettings === selected;
    group.hidden = !visible;
    group.querySelectorAll("input").forEach((input) => { input.disabled = !visible; });
  });
}

function renderSignalSummary(summary = {}) {
  els.signalTotal.textContent = String(summary.total || 0);
  els.signalPending.textContent = String(summary.pending || 0);
  els.signalAccepted.textContent = String(summary.accepted || 0);
  els.signalExcluded.textContent = String(summary.excluded || 0);
}

function standardLabel(signal) {
  const standard = signal.backtest_standard;
  if (!standard) return '<span class="mutedCell">Chưa đặt</span>';
  return `<button class="standardLink" data-select-run="${escapeHtml(standard.id)}" type="button">#${escapeHtml(standard.id)} · ${formatPercent(standard.total_return)}<small>DD ${formatPercent(standard.max_drawdown)}</small></button>`;
}

function renderSignals() {
  if (!signals.length) {
    els.signalsTable.innerHTML = '<tr><td class="empty" colspan="6">Không có tín hiệu theo bộ lọc hiện tại.</td></tr>';
    return;
  }
  els.signalsTable.innerHTML = signals.map((signal) => `
    <tr>
      <td>${escapeHtml((signal.received_at || "").slice(0, 16).replace("T", " "))}<small>${escapeHtml(signal.timeframe || "")}</small></td>
      <td><strong>${escapeHtml(signal.ticker)}</strong><small>${escapeHtml(signal.strategy || "Không nêu chiến lược")}</small></td>
      <td><b class="signalAction ${escapeHtml(signal.action)}">${escapeHtml(signal.action)}</b><small>${escapeHtml(signal.note || signal.rejection_reason || "")}</small></td>
      <td>${standardLabel(signal)}</td>
      <td><select data-signal-category="${escapeHtml(signal.id)}"><option value="watch" ${signal.category === "watch" ? "selected" : ""}>Theo dõi</option><option value="entry" ${signal.category === "entry" ? "selected" : ""}>Điểm vào</option><option value="exit" ${signal.category === "exit" ? "selected" : ""}>Điểm ra</option><option value="research" ${signal.category === "research" ? "selected" : ""}>Nghiên cứu</option><option value="excluded" ${signal.category === "excluded" ? "selected" : ""}>Loại</option></select><small class="signalStatus ${escapeHtml(signal.status)}">${escapeHtml(signal.status)}</small></td>
      <td><div class="signalActions"><button data-accept-signal="${escapeHtml(signal.id)}" type="button">Chấp nhận</button><button data-exclude-signal="${escapeHtml(signal.id)}" type="button">Loại</button><button data-delete-signal="${escapeHtml(signal.id)}" class="miniDanger" type="button">Xóa</button></div></td>
    </tr>
  `).join("");
  els.signalsTable.querySelectorAll("[data-accept-signal]").forEach((button) => {
    button.addEventListener("click", () => classifySignal(button.dataset.acceptSignal, "accepted"));
  });
  els.signalsTable.querySelectorAll("[data-exclude-signal]").forEach((button) => {
    button.addEventListener("click", () => classifySignal(button.dataset.excludeSignal, "excluded"));
  });
  els.signalsTable.querySelectorAll("[data-delete-signal]").forEach((button) => {
    button.addEventListener("click", () => deleteSignal(button.dataset.deleteSignal));
  });
  els.signalsTable.querySelectorAll("[data-select-run]").forEach((button) => {
    button.addEventListener("click", () => selectRun(button.dataset.selectRun));
  });
}

async function loadSignalFilters() {
  const payload = await request("/api/signal-filters");
  const filters = payload.filters || {};
  els.allowedTickers.value = (filters.allowed_tickers || []).join(", ");
  els.allowedStrategies.value = (filters.allowed_strategies || []).join(", ");
  els.allowBuy.checked = Boolean(filters.allow_buy);
  els.allowSell.checked = Boolean(filters.allow_sell);
}

async function loadSignals() {
  const query = new URLSearchParams();
  if (els.signalStatusFilter.value) query.set("status", els.signalStatusFilter.value);
  if (els.signalTickerFilter.value.trim()) query.set("ticker", els.signalTickerFilter.value.trim().toUpperCase());
  const suffix = query.size ? `?${query.toString()}` : "";
  const payload = await request(`/api/signals${suffix}`);
  signals = payload.signals || [];
  renderSignalSummary(payload.summary);
  renderSignals();
}

async function saveSignalFilters(event) {
  event.preventDefault();
  try {
    await request("/api/signal-filters", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        allowed_tickers: els.allowedTickers.value,
        allowed_strategies: els.allowedStrategies.value,
        allow_buy: els.allowBuy.checked,
        allow_sell: els.allowSell.checked,
      }),
    });
    setStatus("Đã lưu điều kiện nhận webhook.", "success");
  } catch (error) {
    setStatus(error.message, "error");
  }
}

async function classifySignal(signalId, status) {
  const category = els.signalsTable.querySelector(`[data-signal-category="${CSS.escape(String(signalId))}"]`)?.value || "watch";
  try {
    await request(`/api/signals/${encodeURIComponent(signalId)}`, {
      method: "PATCH", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status, category: status === "excluded" ? "excluded" : category }),
    });
    await loadSignals();
  } catch (error) {
    setStatus(error.message, "error");
  }
}

async function deleteSignal(signalId) {
  if (!window.confirm("Xóa hẳn tín hiệu này? Thao tác này không thể hoàn tác.")) return;
  try {
    await request(`/api/signals/${encodeURIComponent(signalId)}`, { method: "DELETE" });
    await loadSignals();
  } catch (error) {
    setStatus(error.message, "error");
  }
}

function runName(run) {
  const output = `${(run.symbols || []).join(", ")} · ${run.strategy}`;
  const returnText = run.status === "completed" ? ` · ${formatPercent(run.metrics?.total_return)}` : "";
  return `${output}${returnText}${run.is_standard ? " · CHUẨN" : ""}`;
}

function renderRuns() {
  if (!runs.length) {
    els.runHistory.innerHTML = '<p class="empty">Chưa có kết quả.</p>';
    return;
  }
  els.runHistory.innerHTML = runs.map((run) => `
    <button class="runItem ${String(run.id) === String(activeRunId) ? "active" : ""}" data-run-id="${escapeHtml(run.id)}" type="button">
      <strong>${escapeHtml(runName(run))}</strong>
      <span>${escapeHtml(run.start_date)} → ${escapeHtml(run.end_date)}</span>
      <i class="runState ${escapeHtml(run.status)}">${escapeHtml(run.status)}</i>
    </button>
  `).join("");
  els.runHistory.querySelectorAll("[data-run-id]").forEach((button) => {
    button.addEventListener("click", () => selectRun(button.dataset.runId));
  });
}

async function loadRuns() {
  const payload = await request("/api/backtests");
  runs = payload.backtests || [];
  renderRuns();
}

function metric(label, value) {
  return `<article><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></article>`;
}

function renderMetrics(run) {
  if (run.status !== "completed") {
    els.metrics.innerHTML = `<p class="empty">${escapeHtml(run.error_text || `Trạng thái: ${run.status}`)}</p>`;
    return;
  }
  const data = run.metrics || {};
  els.metrics.innerHTML = [
    metric("Tổng lợi nhuận", formatPercent(data.total_return)),
    metric("CAGR", formatPercent(data.cagr)),
    metric("Max drawdown", formatPercent(data.max_drawdown)),
    metric("Sharpe", Number(data.sharpe || 0).toFixed(2)),
    metric("Vốn cuối", formatVnd(data.ending_equity)),
    metric("Số lệnh", String(data.trade_count || 0)),
    metric("Biến động năm", formatPercent(data.annual_volatility)),
    metric("Nguồn", run.data_source || "vnstock"),
  ].join("");
}

function resetCharts() {
  equityChart?.remove();
  drawdownChart?.remove();
  equityChart = null;
  drawdownChart = null;
  els.equityChart.replaceChildren();
  els.drawdownChart.replaceChildren();
}

function chartOptions(node) {
  const css = getComputedStyle(document.documentElement);
  return {
    width: Math.max(1, node.clientWidth), height: Math.max(1, node.clientHeight),
    layout: {
      background: { type: window.LightweightCharts.ColorType.Solid, color: css.getPropertyValue("--surface").trim() || "#fff" },
      textColor: css.getPropertyValue("--muted").trim() || "#64748b", attributionLogo: false,
    },
    grid: {
      vertLines: { color: css.getPropertyValue("--line").trim() || "#e5e7eb" },
      horzLines: { color: css.getPropertyValue("--line").trim() || "#e5e7eb" },
    },
    rightPriceScale: { borderVisible: false }, timeScale: { borderVisible: false },
  };
}

function drawCharts(points) {
  resetCharts();
  if (!points.length || !window.LightweightCharts) return;
  const css = getComputedStyle(document.documentElement);
  const positive = css.getPropertyValue("--positive").trim() || "#12805c";
  const negative = css.getPropertyValue("--negative").trim() || "#c44343";
  equityChart = window.LightweightCharts.createChart(els.equityChart, chartOptions(els.equityChart));
  const equitySeries = equityChart.addSeries(window.LightweightCharts.AreaSeries, {
    lineColor: positive, topColor: `${positive}45`, bottomColor: `${positive}05`, lineWidth: 2,
  });
  equitySeries.setData(points.map((point) => ({ time: point.date, value: Number(point.equity) })));
  equityChart.timeScale().fitContent();

  let peak = 0;
  const drawdown = points.map((point) => {
    peak = Math.max(peak, Number(point.equity));
    return { time: point.date, value: peak ? (Number(point.equity) / peak - 1) * 100 : 0 };
  });
  drawdownChart = window.LightweightCharts.createChart(els.drawdownChart, chartOptions(els.drawdownChart));
  const drawdownSeries = drawdownChart.addSeries(window.LightweightCharts.AreaSeries, {
    lineColor: negative, topColor: `${negative}0a`, bottomColor: `${negative}45`, lineWidth: 2,
  });
  drawdownSeries.setData(drawdown);
  drawdownChart.timeScale().fitContent();
}

function renderTrades(trades) {
  if (!trades.length) {
    els.trades.innerHTML = '<tr><td class="empty" colspan="6">Chưa có giao dịch.</td></tr>';
    return;
  }
  els.trades.innerHTML = trades.slice().reverse().slice(0, 150).map((trade) => `
    <tr><td>${escapeHtml(trade.date)}</td><td>${escapeHtml(trade.symbol)}</td><td class="${String(trade.side).toLowerCase()}">${escapeHtml(trade.side)}</td><td>${escapeHtml(trade.quantity)}</td><td>${formatVnd(trade.fill_price)}</td><td>${formatVnd(trade.costs)}</td></tr>
  `).join("");
}

function schedulePoll(run) {
  clearTimeout(pollTimer);
  if (!run || !["queued", "running"].includes(run.status)) return;
  pollTimer = setTimeout(async () => {
    try {
      await loadRuns();
      await selectRun(run.id);
    } catch (error) {
      setStatus(error.message, "error");
    }
  }, 3_000);
}

async function selectRun(runId) {
  activeRunId = runId;
  renderRuns();
  const payload = await request(`/api/backtests/${encodeURIComponent(runId)}`);
  const run = payload.backtest;
  els.resultTitle.textContent = runName(run);
  els.downloadTrades.href = `/api/backtests/${encodeURIComponent(run.id)}/trades.csv`;
  els.downloadTrades.hidden = run.status !== "completed";
  els.setStandard.hidden = run.status !== "completed";
  els.setStandard.disabled = Boolean(run.is_standard);
  els.setStandard.textContent = run.is_standard ? "Đang là chuẩn" : "Đặt làm chuẩn";
  els.setStandard.dataset.runId = run.id;
  els.deleteRun.hidden = false;
  els.deleteRun.dataset.runId = run.id;
  renderMetrics(run);
  if (run.status === "completed") {
    drawCharts(payload.equity_curve || []);
    renderTrades(payload.trades || []);
    setStatus(`Đã hoàn tất lần chạy #${run.id}.`, "success");
  } else {
    resetCharts();
    renderTrades([]);
    setStatus(run.error_text || `Lần chạy #${run.id}: ${run.status}.`, run.status === "failed" ? "error" : "");
    schedulePoll(run);
  }
}

async function submitBacktest(event) {
  event.preventDefault();
  const values = Object.fromEntries(new FormData(els.form));
  const numericFields = [
    "initial_cash", "fast_window", "slow_window", "rsi_window", "rsi_entry", "rsi_exit",
    "breakout_window", "breakout_exit_window", "commission_rate", "sell_tax_rate",
    "slippage_bps", "lot_size", "max_participation_rate", "rebalance_interval_days",
  ];
  numericFields.forEach((field) => {
    if (field in values) values[field] = Number(values[field]);
  });
  values.symbols = String(values.symbols).toUpperCase();
  els.runButton.disabled = true;
  setStatus("Đang xếp hàng chạy backtest…");
  try {
    const payload = await request("/api/backtests", {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(values),
    });
    await loadRuns();
    await selectRun(payload.backtest.id);
  } catch (error) {
    setStatus(error.message, "error");
  } finally {
    els.runButton.disabled = false;
  }
}

async function deleteActiveRun() {
  const runId = els.deleteRun.dataset.runId;
  if (!runId || !window.confirm("Xóa lần chạy này và toàn bộ kết quả?")) return;
  try {
    await request(`/api/backtests/${encodeURIComponent(runId)}`, { method: "DELETE" });
    activeRunId = null;
    els.resultTitle.textContent = "Chọn một lần chạy";
    els.metrics.innerHTML = '<p class="empty">Kết quả đã được xóa.</p>';
    els.downloadTrades.hidden = true;
    els.setStandard.hidden = true;
    els.deleteRun.hidden = true;
    resetCharts();
    renderTrades([]);
    await loadRuns();
    if (runs.length) await selectRun(runs[0].id);
  } catch (error) {
    setStatus(error.message, "error");
  }
}

async function setActiveRunAsStandard() {
  const runId = els.setStandard.dataset.runId;
  if (!runId) return;
  try {
    const payload = await request(`/api/backtests/${encodeURIComponent(runId)}/standard`, { method: "POST" });
    await loadRuns();
    await selectRun(payload.backtest.id);
    await loadSignals();
  } catch (error) {
    setStatus(error.message, "error");
  }
}

async function login(event) {
  event.preventDefault();
  els.loginError.hidden = true;
  try {
    const payload = await request("/api/auth/login", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: els.loginUsername.value.trim(), password: els.loginPassword.value }),
    });
    showApp(payload.user);
    await initialise();
  } catch (error) {
    els.loginError.textContent = "Sai tài khoản hoặc mật khẩu.";
    els.loginError.hidden = false;
  }
}

async function logout() {
  await fetch("/api/auth/logout", { method: "POST" });
  showLogin();
}

async function initialise() {
  await loadStrategies();
  await loadSignalFilters();
  await loadSignals();
  await loadRuns();
  els.localPublishCommand.textContent = `python -m vn_equity_backtest publish --results-dir results --symbols FPT --dashboard-url ${window.location.origin} --set-standard`;
  if (runs.length) await selectRun(runs[0].id);
}

els.loginForm.addEventListener("submit", login);
els.logoutButton.addEventListener("click", logout);
els.form.addEventListener("submit", submitBacktest);
els.strategy.addEventListener("change", updateStrategyForm);
els.symbols.addEventListener("input", () => { els.symbols.value = els.symbols.value.toUpperCase(); });
els.deleteRun.addEventListener("click", deleteActiveRun);
els.setStandard.addEventListener("click", setActiveRunAsStandard);
els.signalFiltersForm.addEventListener("submit", saveSignalFilters);
els.signalStatusFilter.addEventListener("change", () => loadSignals().catch((error) => setStatus(error.message, "error")));
els.signalTickerFilter.addEventListener("change", () => loadSignals().catch((error) => setStatus(error.message, "error")));
els.refreshSignals.addEventListener("click", () => loadSignals().catch((error) => setStatus(error.message, "error")));
window.addEventListener("resize", () => {
  if (equityChart) equityChart.resize(Math.max(1, els.equityChart.clientWidth), Math.max(1, els.equityChart.clientHeight));
  if (drawdownChart) drawdownChart.resize(Math.max(1, els.drawdownChart.clientWidth), Math.max(1, els.drawdownChart.clientHeight));
});

(async () => {
  try {
    const payload = await request("/api/auth/me");
    if (!payload.user) return showLogin();
    showApp(payload.user);
    await initialise();
  } catch {
    showLogin();
  }
})();
