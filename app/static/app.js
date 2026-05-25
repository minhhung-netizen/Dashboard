const els = {
  total: document.querySelector("#totalSignals"),
  buy: document.querySelector("#buySignals"),
  sell: document.querySelector("#sellSignals"),
  tickers: document.querySelector("#tickerCount"),
  table: document.querySelector("#signalsTable"),
  openPositionsTable: document.querySelector("#openPositionsTable"),
  closedTradesTable: document.querySelector("#closedTradesTable"),
  invalidSignalsTable: document.querySelector("#invalidSignalsTable"),
  performanceTable: document.querySelector("#performanceTable"),
  manualPortfolioTable: document.querySelector("#manualPortfolioTable"),
  manualPositionForm: document.querySelector("#manualPositionForm"),
  manualTicker: document.querySelector("#manualTicker"),
  manualWeight: document.querySelector("#manualWeight"),
  manualEntryPrice: document.querySelector("#manualEntryPrice"),
  manualCurrentPrice: document.querySelector("#manualCurrentPrice"),
  manualQuantity: document.querySelector("#manualQuantity"),
  manualEntryDate: document.querySelector("#manualEntryDate"),
  manualNote: document.querySelector("#manualNote"),
  manualPortfolioReturn: document.querySelector("#manualPortfolioReturn"),
  manualTotalWeight: document.querySelector("#manualTotalWeight"),
  manualOpenCount: document.querySelector("#manualOpenCount"),
  manualClosedCount: document.querySelector("#manualClosedCount"),
  manualRefreshPrices: document.querySelector("#manualRefreshPrices"),
  closedTradesFilter: document.querySelector("#closedTradesFilter"),
  closedTradesFilterLabel: document.querySelector("#closedTradesFilterLabel"),
  clearClosedTradesFilter: document.querySelector("#clearClosedTradesFilter"),
  watchlistInput: document.querySelector("#watchlistInput"),
  watchlistOnly: document.querySelector("#watchlistOnly"),
  addTickerToWatchlist: document.querySelector("#addTickerToWatchlist"),
  timelineTitle: document.querySelector("#timelineTitle"),
  tickerTimeline: document.querySelector("#tickerTimeline"),
  openPositionRefreshPrices: document.querySelector("#openPositionRefreshPrices"),
  openPositionTickerFilter: document.querySelector("#openPositionTickerFilter"),
  openPositionStrategyFilter: document.querySelector("#openPositionStrategyFilter"),
  openPositionSort: document.querySelector("#openPositionSort"),
  performanceTickerFilter: document.querySelector("#performanceTickerFilter"),
  performanceStrategyFilter: document.querySelector("#performanceStrategyFilter"),
  performanceSort: document.querySelector("#performanceSort"),
  languageSelect: document.querySelector("#languageSelect"),
  themeToggle: document.querySelector("#themeToggle"),
  tabButtons: document.querySelectorAll("[data-tab-target]"),
  tabPanels: document.querySelectorAll("[data-tab-panel]"),
  refresh: document.querySelector("#refreshButton"),
  chartTitle: document.querySelector("#chartTitle"),
  lastUpdated: document.querySelector("#lastUpdated"),
  canvas: document.querySelector("#priceChart"),
  equityCanvas: document.querySelector("#equityChart"),
  manualEquityCanvas: document.querySelector("#manualEquityChart"),
};

const translations = {
  en: {
    webhookLabel: "TradingView Webhook",
    refresh: "Refresh",
    darkMode: "Dark mode",
    lightMode: "Light mode",
    watchlistOnly: "Watchlist only",
    addToWatchlist: "Add to watchlist",
    tickerTimeline: "Ticker Timeline",
    clearFilter: "Clear",
    filteredTrades: "Showing trades for",
    tabOverview: "Overview",
    tabPositions: "Positions",
    tabManualPortfolio: "Manual Portfolio",
    tabPerformance: "Performance",
    tabLogs: "Logs",
    total: "Total",
    buy: "Buy",
    sell: "Sell",
    tickers: "Tickers",
    priceHistory: "Price History",
    noTickerSelected: "No ticker selected",
    waitingWebhook: "Waiting for webhook",
    realtimeFeed: "Realtime Feed",
    signals: "Signals",
    time: "Time",
    ticker: "Ticker",
    side: "Side",
    price: "Price",
    timeframe: "Timeframe",
    strategy: "Strategy",
    strategyPerformance: "Strategy Performance",
    buyToSellResults: "Buy to Sell Results",
    closed: "Closed",
    open: "Open",
    winRate: "Win Rate",
    realized: "Realized",
    openPl: "Open P/L",
    current: "Current",
    openPositions: "Open Positions",
    currentHoldings: "Current Holdings",
    entryPrice: "Entry",
    currentPrice: "Current Price",
    returnPct: "Return",
    holdingDays: "Days Held",
    entryTime: "Entry Time",
    entryDate: "Entry Date",
    exitPrice: "Exit",
    exitTime: "Exit Time",
    holdTime: "Hold Time",
    closedTrades: "Closed Trades",
    tradeHistory: "Trade History",
    manualEntry: "Manual Entry",
    addHolding: "Add Holding",
    addPosition: "Add",
    manualPortfolio: "Manual Portfolio",
    portfolioDetail: "Portfolio Detail",
    manualEquityCurve: "Manual Equity Curve",
    portfolioGrowth: "Portfolio Growth",
    totalWeight: "Weight",
    weight: "Weight",
    quantity: "Quantity",
    status: "Status",
    note: "Note",
    save: "Save",
    close: "Close",
    closedStatus: "Closed",
    openStatus: "Open",
    noManualPositions: "No manual positions yet",
    refreshPrices: "Refresh prices",
    refreshPricesFailed: "Could not refresh market prices",
    closeManualConfirm: "Close this manual position?",
    closeManualPricePrompt: "Enter close price",
    closeManualInvalidPrice: "Close price must be greater than 0",
    deleteManualConfirm: "Delete this manual position?",
    manualSaveFailed: "Could not save manual position",
    manualCloseFailed: "Could not close manual position",
    manualDeleteFailed: "Could not delete manual position",
    equityCurve: "Equity Curve",
    closedTradeGrowth: "Closed Trade Growth",
    invalidSignalLog: "Invalid Signal Log",
    ignoredAlerts: "Ignored Alerts",
    reason: "Reason",
    sortCurrentDesc: "Current desc",
    sortCurrentAsc: "Current asc",
    sortRealizedDesc: "Realized desc",
    sortRealizedAsc: "Realized asc",
    sortWinDesc: "Win rate desc",
    sortReturnDesc: "Return desc",
    sortReturnAsc: "Return asc",
    sortCurrentPriceDesc: "Current price desc",
    sortCurrentPriceAsc: "Current price asc",
    sortEntryNewest: "Entry newest",
    sortEntryOldest: "Entry oldest",
    sortTickerAsc: "Ticker A-Z",
    sortStrategyAsc: "Strategy A-Z",
    noTrades: "No completed or open trades yet",
    noOpenPositions: "No open positions",
    noClosedTrades: "No closed trades yet",
    noInvalidSignals: "No invalid signals",
    duplicateWebhook: "Duplicate webhook",
    sellWithoutOpenBuy: "Sell without open buy",
    missingBuyPrice: "Missing buy price",
    missingSellPrice: "Missing sell price",
    positionAlreadyOpen: "Position already open",
    noSignals: "No signals yet",
    noTimeline: "No timeline for this ticker",
    noHistory: "No price history available",
    delete: "Delete",
    deleteTitle: "Delete signal",
    deleteConfirm: "Delete this signal?",
    deleteFailed: "Could not delete signal",
    performanceTickerPlaceholder: "Ticker",
    performanceStrategyPlaceholder: "Strategy",
    openPositionTickerPlaceholder: "Ticker",
    openPositionStrategyPlaceholder: "Strategy",
  },
  vi: {
    webhookLabel: "Webhook TradingView",
    refresh: "Làm mới",
    darkMode: "Chế độ tối",
    lightMode: "Chế độ sáng",
    watchlistOnly: "Chỉ watchlist",
    addToWatchlist: "Thêm watchlist",
    tickerTimeline: "Timeline mã",
    clearFilter: "Xóa lọc",
    filteredTrades: "Đang xem giao dịch của",
    tabOverview: "Tổng quan",
    tabPositions: "Vị thế",
    tabManualPortfolio: "Danh mục tay",
    tabPerformance: "Hiệu suất",
    tabLogs: "Nhật ký",
    total: "Tổng",
    buy: "Mua",
    sell: "Bán",
    tickers: "Mã CP",
    priceHistory: "Lịch sử giá",
    noTickerSelected: "Chưa chọn mã",
    waitingWebhook: "Đang chờ webhook",
    realtimeFeed: "Tín hiệu realtime",
    signals: "Tín hiệu",
    time: "Thời gian",
    ticker: "Mã",
    side: "Chiều",
    price: "Giá",
    timeframe: "Khung TG",
    strategy: "Chiến lược",
    strategyPerformance: "Hiệu suất chiến lược",
    buyToSellResults: "Kết quả Mua đến Bán",
    closed: "Đã đóng",
    open: "Đang mở",
    winRate: "Tỷ lệ thắng",
    realized: "Đã chốt",
    openPl: "Lãi/lỗ mở",
    current: "Hiện tại",
    openPositions: "Vị thế đang mở",
    currentHoldings: "Danh mục hiện tại",
    entryPrice: "Giá vào",
    currentPrice: "Giá hiện tại",
    returnPct: "Lãi/lỗ",
    holdingDays: "Số ngày giữ",
    entryTime: "Thời gian vào",
    entryDate: "Ngày vào",
    exitPrice: "Giá bán",
    exitTime: "Thời gian bán",
    holdTime: "Thời gian giữ",
    closedTrades: "Lệnh đã đóng",
    tradeHistory: "Lịch sử giao dịch",
    manualEntry: "Nhập tay",
    addHolding: "Thêm mã nắm giữ",
    addPosition: "Thêm",
    manualPortfolio: "Danh mục tay",
    portfolioDetail: "Chi tiết danh mục",
    manualEquityCurve: "Đường vốn danh mục tay",
    portfolioGrowth: "Tăng trưởng danh mục",
    totalWeight: "Tỷ trọng",
    weight: "Tỷ trọng",
    quantity: "Số lượng",
    status: "Trạng thái",
    note: "Ghi chú",
    save: "Lưu",
    close: "Đóng",
    closedStatus: "Đã đóng",
    openStatus: "Đang mở",
    noManualPositions: "Chưa có danh mục tay",
    refreshPrices: "Cập nhật giá",
    refreshPricesFailed: "Không thể cập nhật giá thị trường",
    closeManualConfirm: "Đóng vị thế tay này?",
    closeManualPricePrompt: "Nhập giá đóng",
    closeManualInvalidPrice: "Giá đóng phải lớn hơn 0",
    deleteManualConfirm: "Xóa vị thế tay này?",
    manualSaveFailed: "Không thể lưu vị thế tay",
    manualCloseFailed: "Không thể đóng vị thế tay",
    manualDeleteFailed: "Không thể xóa vị thế tay",
    equityCurve: "Đường vốn",
    closedTradeGrowth: "Tăng trưởng lệnh đã đóng",
    invalidSignalLog: "Log tín hiệu lỗi",
    ignoredAlerts: "Cảnh báo bị bỏ qua",
    reason: "Lý do",
    sortCurrentDesc: "Hiện tại giảm dần",
    sortCurrentAsc: "Hiện tại tăng dần",
    sortRealizedDesc: "Đã chốt giảm dần",
    sortRealizedAsc: "Đã chốt tăng dần",
    sortWinDesc: "Tỷ lệ thắng giảm dần",
    sortReturnDesc: "Lãi/lỗ giảm dần",
    sortReturnAsc: "Lãi/lỗ tăng dần",
    sortCurrentPriceDesc: "Giá hiện tại giảm dần",
    sortCurrentPriceAsc: "Giá hiện tại tăng dần",
    sortEntryNewest: "Ngày vào mới nhất",
    sortEntryOldest: "Ngày vào cũ nhất",
    sortTickerAsc: "Mã A-Z",
    sortStrategyAsc: "Chiến lược A-Z",
    noTrades: "Chưa có lệnh đã đóng hoặc đang mở",
    noOpenPositions: "Không có vị thế đang mở",
    noClosedTrades: "Chưa có lệnh đã đóng",
    noInvalidSignals: "Không có tín hiệu lỗi",
    duplicateWebhook: "Webhook trùng",
    sellWithoutOpenBuy: "Bán khi chưa có mua",
    missingBuyPrice: "Thiếu giá mua",
    missingSellPrice: "Thiếu giá bán",
    positionAlreadyOpen: "Vị thế đã mở",
    noSignals: "Chưa có tín hiệu",
    noTimeline: "Chưa có timeline cho mã này",
    noHistory: "Chưa có lịch sử giá",
    delete: "Xóa",
    deleteTitle: "Xóa tín hiệu",
    deleteConfirm: "Xóa tín hiệu này?",
    deleteFailed: "Không thể xóa tín hiệu",
    performanceTickerPlaceholder: "Mã",
    performanceStrategyPlaceholder: "Chiến lược",
    openPositionTickerPlaceholder: "Mã",
    openPositionStrategyPlaceholder: "Chiến lược",
  },
};

const state = {
  language: localStorage.getItem("dashboardLanguage") || "en",
  theme: localStorage.getItem("dashboardTheme") || "light",
  activeTab: localStorage.getItem("dashboardActiveTab") || "overview",
  selectedTicker: "",
  watchlist: loadWatchlist(),
  watchlistOnly: localStorage.getItem("dashboardWatchlistOnly") === "true",
  signals: [],
  openTrades: [],
  closedTrades: [],
  closedTradeFilter: null,
  manualPortfolio: { positions: [], equity_curve: [], summary: {} },
};

function cssVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function t(key) {
  return translations[state.language]?.[key] || translations.en[key] || key;
}

function numberValue(value) {
  return value === null || value === undefined || Number.isNaN(Number(value))
    ? Number.NEGATIVE_INFINITY
    : Number(value);
}

function loadWatchlist() {
  return parseWatchlist(localStorage.getItem("dashboardWatchlist") || "");
}

function parseWatchlist(value) {
  return [
    ...new Set(
      String(value || "")
        .split(/[,\s]+/)
        .map((ticker) => ticker.trim().toUpperCase())
        .filter(Boolean)
    ),
  ];
}

function saveWatchlist() {
  localStorage.setItem("dashboardWatchlist", state.watchlist.join(","));
}

function applyTranslations() {
  document.documentElement.lang = state.language;
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });
  els.refresh.title = t("refresh");
  els.openPositionTickerFilter.placeholder = t("openPositionTickerPlaceholder");
  els.openPositionStrategyFilter.placeholder = t("openPositionStrategyPlaceholder");
  els.performanceTickerFilter.placeholder = t("performanceTickerPlaceholder");
  els.performanceStrategyFilter.placeholder = t("performanceStrategyPlaceholder");
  if (!state.selectedTicker) {
    els.chartTitle.textContent = t("noTickerSelected");
  }
  if (els.lastUpdated.dataset.empty === "true") {
    els.lastUpdated.textContent = t("waitingWebhook");
  }
  updateClosedTradesFilterLabel();
  updateThemeButton();
}

function applyTheme() {
  document.documentElement.dataset.theme = state.theme;
  updateThemeButton();
  if (state.selectedTicker) {
    renderChart(state.selectedTicker);
  }
  if (state.activeTab === "performance") {
    drawEquityCurve(state.closedTrades);
  }
  if (state.activeTab === "manualPortfolio") {
    drawManualEquityCurve(state.manualPortfolio.equity_curve || []);
  }
}

function updateThemeButton() {
  const isDark = state.theme === "dark";
  els.themeToggle.textContent = isDark ? t("lightMode") : t("darkMode");
  els.themeToggle.title = isDark ? t("lightMode") : t("darkMode");
}

function setActiveTab(tabName) {
  const exists = [...els.tabButtons].some((button) => button.dataset.tabTarget === tabName);
  if (!exists) {
    tabName = "overview";
  }
  state.activeTab = tabName;
  localStorage.setItem("dashboardActiveTab", tabName);
  els.tabButtons.forEach((button) => {
    const active = button.dataset.tabTarget === tabName;
    button.classList.toggle("active", active);
    button.setAttribute("aria-selected", String(active));
  });
  els.tabPanels.forEach((panel) => {
    panel.classList.toggle("active", panel.dataset.tabPanel === tabName);
  });
  if (tabName === "overview" && state.selectedTicker) {
    renderChart(state.selectedTicker);
  }
  if (tabName === "performance") {
    drawEquityCurve(state.closedTrades);
  }
  if (tabName === "manualPortfolio") {
    drawManualEquityCurve(state.manualPortfolio.equity_curve || []);
  }
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return response.json();
}

async function refresh() {
  const query = "";
  const performanceQuery = buildPerformanceQuery();
  const [summary, signalsPayload, performancePayload, invalidPayload, manualPayload] = await Promise.all([
    fetchJson("/api/summary"),
    fetchJson(`/api/signals${query}`),
    fetchJson(`/api/performance${performanceQuery}`),
    fetchJson("/api/invalid-signals"),
    fetchJson("/api/manual-portfolio"),
  ]);

  state.signals = filterSignalsForWatchlist(signalsPayload.signals || []);
  renderSummary(summary);
  renderSignals();
  state.openTrades = performancePayload.open_trades || [];
  renderOpenPositions();
  state.closedTrades = performancePayload.closed_trades || [];
  renderClosedTrades(state.closedTrades);
  if (state.activeTab === "performance") {
    drawEquityCurve(state.closedTrades);
  }
  renderInvalidSignals([
    ...(performancePayload.ignored_signals || []).map((item) => ({
      ...item,
      received_at: "",
      timeframe: "",
    })),
    ...(invalidPayload.invalid_signals || []),
  ]);
  renderPerformance(sortPerformance(performancePayload.strategies || []));
  state.manualPortfolio = manualPayload;
  renderManualPortfolio(manualPayload);

  const firstTicker = state.selectedTicker || state.signals[0]?.ticker || "";
  if (firstTicker) {
    await renderChart(firstTicker);
  } else {
    state.selectedTicker = "";
    els.chartTitle.textContent = t("noTickerSelected");
    renderTickerTimeline("");
    clearChart(t("noTickerSelected"));
  }
}

function filterSignalsForWatchlist(signals) {
  if (!state.watchlistOnly) return signals;
  if (!state.watchlist.length) return [];
  const allowed = new Set(state.watchlist);
  return signals.filter((signal) => allowed.has(String(signal.ticker || "").toUpperCase()));
}

function renderManualPortfolio(payload) {
  const summary = payload.summary || {};
  const positions = payload.positions || [];
  els.manualPortfolioReturn.innerHTML = formatSignedPercent(summary.portfolio_return_pct);
  els.manualTotalWeight.textContent = formatPercent(summary.total_weight_pct || 0);
  els.manualOpenCount.textContent = summary.open_count ?? 0;
  els.manualClosedCount.textContent = summary.closed_count ?? 0;
  drawManualEquityCurve(payload.equity_curve || []);

  if (!positions.length) {
    els.manualPortfolioTable.innerHTML = `<tr><td class="empty" colspan="11">${t("noManualPositions")}</td></tr>`;
    return;
  }

  els.manualPortfolioTable.innerHTML = positions
    .map((position) => {
      const status = position.status === "closed" ? "closed" : "open";
      const isOpen = status === "open";
      const markPrice = position.mark_price ?? position.current_price;
      return `
        <tr>
          <td><strong>${escapeHtml(position.ticker)}</strong></td>
          <td>${formatPercent(position.weight_pct)}</td>
          <td>${formatPrice(position.entry_price)}</td>
          <td>${formatPrice(markPrice)}</td>
          <td>${formatSignedPercent(position.return_pct)}</td>
          <td>${formatPrice(position.quantity)}</td>
          <td><span class="statusBadge ${status}">${escapeHtml(isOpen ? t("openStatus") : t("closedStatus"))}</span></td>
          <td>${formatDateOnly(position.entry_date)}</td>
          <td>${formatHoldingDaysBetween(position.entry_date, isOpen ? null : position.closed_at)}</td>
          <td>${escapeHtml(position.note || "-")}</td>
          <td>
            <div class="portfolioActions">
              ${isOpen ? `
                <input
                  type="number"
                  min="0.001"
                  step="0.001"
                  aria-label="${escapeHtml(t("closeManualPricePrompt"))}"
                  value="${escapeHtml(rawNumber(markPrice))}"
                  data-manual-close-price-input="${position.id}"
                />
                <button class="deleteButton" type="button" data-manual-close-id="${position.id}">${escapeHtml(t("close"))}</button>
              ` : ""}
              <button class="deleteButton" type="button" data-manual-delete-id="${position.id}">${escapeHtml(t("delete"))}</button>
            </div>
          </td>
        </tr>
      `;
    })
    .join("");

  els.manualPortfolioTable.querySelectorAll("[data-manual-close-id]").forEach((button) => {
    button.addEventListener("click", () => closeManualPosition(button.dataset.manualCloseId));
  });
  els.manualPortfolioTable.querySelectorAll("[data-manual-delete-id]").forEach((button) => {
    button.addEventListener("click", () => deleteManualPosition(button.dataset.manualDeleteId));
  });
}

async function addManualPosition(event) {
  event.preventDefault();
  const body = {
    ticker: els.manualTicker.value.trim().toUpperCase(),
    weight_pct: Number(els.manualWeight.value),
    entry_price: Number(els.manualEntryPrice.value),
    current_price: optionalNumber(els.manualCurrentPrice.value),
    quantity: optionalNumber(els.manualQuantity.value),
    entry_date: localDateToIsoDate(els.manualEntryDate.value),
    note: els.manualNote.value.trim() || null,
  };
  const response = await fetch("/api/manual-portfolio", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    window.alert(t("manualSaveFailed"));
    return;
  }
  els.manualPositionForm.reset();
  await refresh();
}

async function closeManualPosition(positionId) {
  const input = els.manualPortfolioTable.querySelector(
    `[data-manual-close-price-input="${CSS.escape(String(positionId))}"]`
  );
  const rawPrice = input?.value || "";
  const price = parsePriceInput(rawPrice);
  if (!Number.isFinite(price) || price <= 0) {
    window.alert(t("closeManualInvalidPrice"));
    input?.focus();
    return;
  }
  const response = await fetch(`/api/manual-portfolio/${encodeURIComponent(positionId)}/close`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ exit_price: price }),
  });
  if (!response.ok) {
    window.alert(t("manualCloseFailed"));
    return;
  }
  await refresh();
}

async function deleteManualPosition(positionId) {
  if (!window.confirm(t("deleteManualConfirm"))) {
    return;
  }
  const response = await fetch(`/api/manual-portfolio/${encodeURIComponent(positionId)}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    window.alert(t("manualDeleteFailed"));
    return;
  }
  await refresh();
}

async function refreshManualMarketPrices() {
  const response = await fetch("/api/manual-portfolio/refresh-prices", {
    method: "POST",
  });
  if (!response.ok) {
    window.alert(t("refreshPricesFailed"));
    return;
  }
  await refresh();
}

async function refreshOpenPositionMarketPrices() {
  const response = await fetch("/api/open-positions/refresh-prices", {
    method: "POST",
  });
  if (!response.ok) {
    window.alert(t("refreshPricesFailed"));
    return;
  }
  await refresh();
}

function buildPerformanceQuery() {
  const params = new URLSearchParams();
  const ticker = els.performanceTickerFilter.value.trim().toUpperCase();
  const strategy = els.performanceStrategyFilter.value.trim();
  if (ticker) params.set("ticker", ticker);
  if (strategy) params.set("strategy", strategy);
  const query = params.toString();
  return query ? `?${query}` : "";
}

function sortPerformance(strategies) {
  const sortMode = els.performanceSort.value;
  const sorted = [...strategies];

  sorted.sort((left, right) => {
    switch (sortMode) {
      case "current_asc":
        return numberValue(left.current_return_pct) - numberValue(right.current_return_pct);
      case "realized_desc":
        return numberValue(right.realized_return_pct) - numberValue(left.realized_return_pct);
      case "realized_asc":
        return numberValue(left.realized_return_pct) - numberValue(right.realized_return_pct);
      case "win_desc":
        return numberValue(right.win_rate_pct) - numberValue(left.win_rate_pct);
      case "ticker_asc":
        return String(left.ticker).localeCompare(String(right.ticker));
      case "strategy_asc":
        return String(left.strategy).localeCompare(String(right.strategy));
      case "current_desc":
      default:
        return numberValue(right.current_return_pct) - numberValue(left.current_return_pct);
    }
  });
  return sorted;
}

function filterOpenPositions(openTrades) {
  const tickerFilter = els.openPositionTickerFilter.value.trim().toUpperCase();
  const strategyFilter = els.openPositionStrategyFilter.value.trim().toLowerCase();
  return openTrades.filter((trade) => {
    const tickerMatches = !tickerFilter || String(trade.ticker || "").includes(tickerFilter);
    const strategyMatches =
      !strategyFilter || String(trade.strategy || "").toLowerCase().includes(strategyFilter);
    return tickerMatches && strategyMatches;
  });
}

function sortOpenPositions(openTrades) {
  const sortMode = els.openPositionSort.value;
  const sorted = [...openTrades];
  sorted.sort((left, right) => {
    switch (sortMode) {
      case "return_asc":
        return numberValue(left.return_pct) - numberValue(right.return_pct);
      case "current_price_desc":
        return numberValue(right.exit_price) - numberValue(left.exit_price);
      case "current_price_asc":
        return numberValue(left.exit_price) - numberValue(right.exit_price);
      case "entry_newest":
        return String(right.entry_time || "").localeCompare(String(left.entry_time || ""));
      case "entry_oldest":
        return String(left.entry_time || "").localeCompare(String(right.entry_time || ""));
      case "ticker_asc":
        return String(left.ticker || "").localeCompare(String(right.ticker || ""));
      case "strategy_asc":
        return String(left.strategy || "").localeCompare(String(right.strategy || ""));
      case "return_desc":
      default:
        return numberValue(right.return_pct) - numberValue(left.return_pct);
    }
  });
  return sorted;
}

function renderPerformance(strategies) {
  if (!strategies.length) {
    els.performanceTable.innerHTML = `<tr><td class="empty" colspan="8">${t("noTrades")}</td></tr>`;
    return;
  }

  els.performanceTable.innerHTML = strategies
    .map((strategy) => `
      <tr class="clickableRow" data-performance-ticker="${escapeHtml(strategy.ticker)}" data-performance-strategy="${escapeHtml(strategy.strategy)}">
        <td><strong>${escapeHtml(strategy.ticker)}</strong></td>
        <td><strong>${escapeHtml(strategy.strategy)}</strong></td>
        <td>${strategy.closed_trades}</td>
        <td>${strategy.open_trades}</td>
        <td>${formatPercent(strategy.win_rate_pct)}</td>
        <td>${formatSignedPercent(strategy.realized_return_pct)}</td>
        <td>${formatSignedPercent(strategy.open_return_avg_pct)}</td>
        <td>${formatSignedPercent(strategy.current_return_pct)}</td>
      </tr>
    `)
    .join("");

  els.performanceTable.querySelectorAll("[data-performance-ticker]").forEach((row) => {
    row.addEventListener("click", () => {
      applyClosedTradeFilter(row.dataset.performanceTicker, row.dataset.performanceStrategy);
    });
  });
}

function renderOpenPositions() {
  const openTrades = sortOpenPositions(filterOpenPositions(state.openTrades));
  if (!openTrades.length) {
    els.openPositionsTable.innerHTML = `<tr><td class="empty" colspan="7">${t("noOpenPositions")}</td></tr>`;
    return;
  }

  els.openPositionsTable.innerHTML = openTrades
    .map((trade) => `
      <tr data-ticker="${escapeHtml(trade.ticker)}">
        <td><strong>${escapeHtml(trade.ticker)}</strong></td>
        <td><strong>${escapeHtml(trade.strategy)}</strong></td>
        <td>${formatPrice(trade.entry_price)}</td>
        <td>${formatPrice(trade.exit_price)}</td>
        <td>${formatSignedPercent(trade.return_pct)}</td>
        <td>${formatHoldingDaysBetween(trade.entry_time)}</td>
        <td>${formatDate(trade.entry_time)}</td>
      </tr>
    `)
    .join("");

  els.openPositionsTable.querySelectorAll("[data-ticker]").forEach((row) => {
    row.addEventListener("click", () => renderChart(row.dataset.ticker));
  });
}

function renderClosedTrades(closedTrades) {
  const filtered = filterClosedTrades(closedTrades);
  updateClosedTradesFilterLabel();
  const sorted = [...filtered].sort((left, right) =>
    String(right.exit_time || "").localeCompare(String(left.exit_time || ""))
  );

  if (!sorted.length) {
    els.closedTradesTable.innerHTML = `<tr><td class="empty" colspan="7">${t("noClosedTrades")}</td></tr>`;
    return;
  }

  els.closedTradesTable.innerHTML = sorted
    .map((trade) => `
      <tr data-ticker="${escapeHtml(trade.ticker)}">
        <td><strong>${escapeHtml(trade.ticker)}</strong></td>
        <td><strong>${escapeHtml(trade.strategy)}</strong></td>
        <td>${formatPrice(trade.entry_price)}</td>
        <td>${formatPrice(trade.exit_price)}</td>
        <td>${formatSignedPercent(trade.return_pct)}</td>
        <td>${formatDuration(trade.holding_seconds)}</td>
        <td>${formatDate(trade.exit_time)}</td>
      </tr>
    `)
    .join("");

  els.closedTradesTable.querySelectorAll("[data-ticker]").forEach((row) => {
    row.addEventListener("click", () => renderChart(row.dataset.ticker));
  });
}

function filterClosedTrades(closedTrades) {
  if (!state.closedTradeFilter) return closedTrades;
  const ticker = state.closedTradeFilter.ticker;
  const strategy = state.closedTradeFilter.strategy;
  return closedTrades.filter(
    (trade) => trade.ticker === ticker && trade.strategy === strategy
  );
}

function applyClosedTradeFilter(ticker, strategy) {
  state.closedTradeFilter = { ticker, strategy };
  renderClosedTrades(state.closedTrades);
  setActiveTab("positions");
}

function clearClosedTradeFilter() {
  state.closedTradeFilter = null;
  renderClosedTrades(state.closedTrades);
}

function updateClosedTradesFilterLabel() {
  if (!state.closedTradeFilter) {
    els.closedTradesFilter.hidden = true;
    els.closedTradesFilterLabel.textContent = "";
    return;
  }
  els.closedTradesFilter.hidden = false;
  els.closedTradesFilterLabel.textContent =
    `${t("filteredTrades")} ${state.closedTradeFilter.ticker} / ${state.closedTradeFilter.strategy}`;
}

function updateWatchlistControls() {
  els.watchlistInput.value = state.watchlist.join(",");
  els.watchlistOnly.checked = state.watchlistOnly;
}

function updateWatchlistFromInput() {
  state.watchlist = parseWatchlist(els.watchlistInput.value);
  saveWatchlist();
  refresh();
}

function toggleWatchlistOnly() {
  state.watchlistOnly = els.watchlistOnly.checked;
  localStorage.setItem("dashboardWatchlistOnly", String(state.watchlistOnly));
  refresh();
}

function addSelectedTickerToWatchlist() {
  const ticker = (state.selectedTicker || "").trim().toUpperCase();
  if (!ticker) return;
  if (!state.watchlist.includes(ticker)) {
    state.watchlist.push(ticker);
    saveWatchlist();
    updateWatchlistControls();
  }
}

function renderInvalidSignals(invalidSignals) {
  if (!invalidSignals.length) {
    els.invalidSignalsTable.innerHTML = `<tr><td class="empty" colspan="6">${t("noInvalidSignals")}</td></tr>`;
    return;
  }

  els.invalidSignalsTable.innerHTML = invalidSignals
    .slice(0, 100)
    .map((signal) => `
      <tr>
        <td>${formatSignalTime(signal)}</td>
        <td><strong>${escapeHtml(signal.ticker || "-")}</strong></td>
        <td>${escapeHtml(signal.action || "-")}</td>
        <td>${escapeHtml(signal.timeframe || "-")}</td>
        <td>${escapeHtml(signal.strategy || "-")}</td>
        <td>${escapeHtml(formatReason(signal.reason))}</td>
      </tr>
    `)
    .join("");
}

function formatReason(reason) {
  const key = {
    duplicate_webhook: "duplicateWebhook",
    sell_without_open_buy: "sellWithoutOpenBuy",
    missing_buy_price: "missingBuyPrice",
    missing_sell_price: "missingSellPrice",
    position_already_open: "positionAlreadyOpen",
  }[reason];
  return key ? t(key) : reason || "-";
}

function drawEquityCurve(closedTrades) {
  const canvas = els.equityCanvas;
  const ctx = canvas.getContext("2d");
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.max(1, Math.floor(rect.width * dpr));
  canvas.height = Math.max(1, Math.floor(rect.height * dpr));
  ctx.scale(dpr, dpr);
  ctx.clearRect(0, 0, rect.width, rect.height);

  const sorted = [...closedTrades].sort((left, right) =>
    String(left.exit_time || "").localeCompare(String(right.exit_time || ""))
  );
  if (!sorted.length) {
    ctx.fillStyle = cssVar("--muted") || "#66727a";
    ctx.font = "14px system-ui";
    ctx.fillText(t("noClosedTrades"), 18, 38);
    return;
  }

  const points = [{ value: 100, label: "Start" }];
  sorted.forEach((trade) => {
    const previous = points[points.length - 1].value;
    points.push({
      value: previous * (1 + Number(trade.return_pct || 0) / 100),
      label: trade.ticker,
    });
  });

  const pad = { top: 24, right: 48, bottom: 30, left: 18 };
  const width = rect.width - pad.left - pad.right;
  const height = rect.height - pad.top - pad.bottom;
  const min = Math.min(...points.map((point) => point.value));
  const max = Math.max(...points.map((point) => point.value));
  const range = max - min || 1;

  ctx.strokeStyle = cssVar("--line") || "#dbe2df";
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i += 1) {
    const y = pad.top + (height / 4) * i;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(rect.width - pad.right + 6, y);
    ctx.stroke();
    const label = max - (range / 4) * i;
    ctx.fillStyle = cssVar("--muted") || "#66727a";
    ctx.font = "12px system-ui";
    ctx.fillText(label.toFixed(1), rect.width - pad.right + 10, y + 4);
  }

  ctx.strokeStyle = cssVar("--accent") || "#245c7a";
  ctx.lineWidth = 2;
  ctx.beginPath();
  points.forEach((point, index) => {
    const x = pad.left + (width / Math.max(1, points.length - 1)) * index;
    const y = pad.top + height - ((point.value - min) / range) * height;
    if (index === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  });
  ctx.stroke();

  const last = points[points.length - 1];
  ctx.fillStyle = cssVar("--ink") || "#152025";
  ctx.font = "700 12px system-ui";
  ctx.fillText(`${last.value.toFixed(2)}`, pad.left, rect.height - 9);
}

function drawManualEquityCurve(curve) {
  const canvas = els.manualEquityCanvas;
  const ctx = canvas.getContext("2d");
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.max(1, Math.floor(rect.width * dpr));
  canvas.height = Math.max(1, Math.floor(rect.height * dpr));
  ctx.scale(dpr, dpr);
  ctx.clearRect(0, 0, rect.width, rect.height);

  const points = (curve || [])
    .map((point) => ({
      value: Number(point.value),
      label: point.time || "",
    }))
    .filter((point) => Number.isFinite(point.value));

  if (!points.length) {
    ctx.fillStyle = cssVar("--muted") || "#66727a";
    ctx.font = "14px system-ui";
    ctx.fillText(t("noManualPositions"), 18, 38);
    return;
  }

  const pad = { top: 24, right: 48, bottom: 30, left: 18 };
  const width = rect.width - pad.left - pad.right;
  const height = rect.height - pad.top - pad.bottom;
  const min = Math.min(...points.map((point) => point.value), 100);
  const max = Math.max(...points.map((point) => point.value), 100);
  const range = max - min || 1;

  ctx.strokeStyle = cssVar("--line") || "#dbe2df";
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i += 1) {
    const y = pad.top + (height / 4) * i;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(rect.width - pad.right + 6, y);
    ctx.stroke();
    const label = max - (range / 4) * i;
    ctx.fillStyle = cssVar("--muted") || "#66727a";
    ctx.font = "12px system-ui";
    ctx.fillText(label.toFixed(1), rect.width - pad.right + 10, y + 4);
  }

  ctx.strokeStyle = cssVar("--accent") || "#245c7a";
  ctx.lineWidth = 2;
  ctx.beginPath();
  points.forEach((point, index) => {
    const x = pad.left + (width / Math.max(1, points.length - 1)) * index;
    const y = pad.top + height - ((point.value - min) / range) * height;
    if (index === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  });
  ctx.stroke();

  const last = points[points.length - 1];
  ctx.fillStyle = cssVar("--ink") || "#152025";
  ctx.font = "700 12px system-ui";
  ctx.fillText(`${last.value.toFixed(2)}`, pad.left, rect.height - 9);
}

function renderSummary(summary) {
  const visibleSummary = state.watchlistOnly ? summarizeSignals(state.signals) : summary;
  els.total.textContent = visibleSummary.total ?? 0;
  els.buy.textContent = visibleSummary.buy_count ?? 0;
  els.sell.textContent = visibleSummary.sell_count ?? 0;
  els.tickers.textContent = visibleSummary.tickers ?? 0;
  els.lastUpdated.textContent = summary.latest_received_at
    ? formatDate(summary.latest_received_at)
    : t("waitingWebhook");
  els.lastUpdated.dataset.empty = summary.latest_received_at ? "false" : "true";
}

function summarizeSignals(signals) {
  const tickers = new Set();
  let buyCount = 0;
  let sellCount = 0;
  signals.forEach((signal) => {
    if (signal.ticker) tickers.add(signal.ticker);
    const action = String(signal.action || "").toLowerCase();
    if (action === "buy") buyCount += 1;
    if (action === "sell") sellCount += 1;
  });
  return {
    total: signals.length,
    buy_count: buyCount,
    sell_count: sellCount,
    tickers: tickers.size,
  };
}

function renderSignals() {
  if (!state.signals.length) {
    els.table.innerHTML = `<tr><td class="empty" colspan="7">${t("noSignals")}</td></tr>`;
    return;
  }

  els.table.innerHTML = state.signals
    .map((signal) => {
      const action = (signal.action || "").toLowerCase();
      return `
        <tr data-ticker="${escapeHtml(signal.ticker)}">
          <td>${formatSignalTime(signal)}</td>
          <td><strong>${escapeHtml(signal.ticker)}</strong></td>
          <td><span class="side ${action}">${escapeHtml(signal.action)}</span></td>
          <td>${formatPrice(signal.price)}</td>
          <td>${escapeHtml(signal.timeframe || "-")}</td>
          <td>${escapeHtml(signal.strategy || "-")}</td>
          <td>
            <button class="deleteButton" type="button" data-delete-id="${signal.id}" title="${escapeHtml(t("deleteTitle"))}" aria-label="${escapeHtml(`${t("deleteTitle")} ${signal.id}`)}">${escapeHtml(t("delete"))}</button>
          </td>
        </tr>
      `;
    })
    .join("");

  document.querySelectorAll("[data-ticker]").forEach((row) => {
    row.addEventListener("click", () => renderChart(row.dataset.ticker));
  });
  document.querySelectorAll("[data-delete-id]").forEach((button) => {
    button.addEventListener("click", async (event) => {
      event.stopPropagation();
      await deleteSignal(button.dataset.deleteId);
    });
  });
}

async function deleteSignal(signalId) {
  if (!window.confirm(t("deleteConfirm"))) {
    return;
  }
  const response = await fetch(`/api/signals/${encodeURIComponent(signalId)}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    window.alert(t("deleteFailed"));
    return;
  }
  await refresh();
}

async function renderChart(ticker) {
  state.selectedTicker = ticker;
  els.chartTitle.textContent = ticker;
  renderTickerTimeline(ticker);
  const payload = await fetchJson(`/api/chart/${encodeURIComponent(ticker)}`);
  drawCandles(
    normalizeHistory(payload.history || []),
    normalizeMarkers(payload.markers || [])
  );
}

function renderTickerTimeline(ticker) {
  const normalizedTicker = String(ticker || "").toUpperCase();
  if (!normalizedTicker) {
    els.timelineTitle.textContent = t("noTickerSelected");
    els.tickerTimeline.innerHTML = `<div class="empty">${t("noTickerSelected")}</div>`;
    return;
  }

  els.timelineTitle.textContent = normalizedTicker;
  const timeline = state.signals
    .filter((signal) => String(signal.ticker || "").toUpperCase() === normalizedTicker)
    .sort((left, right) => signalTimeSortValue(right) - signalTimeSortValue(left));

  if (!timeline.length) {
    els.tickerTimeline.innerHTML = `<div class="empty">${t("noTimeline")}</div>`;
    return;
  }

  els.tickerTimeline.innerHTML = timeline
    .slice(0, 30)
    .map((signal) => {
      const action = String(signal.action || "").toLowerCase();
      return `
        <div class="timelineItem">
          <span class="side ${escapeHtml(action)}">${escapeHtml(signal.action || "-")}</span>
          <div>
            <strong>${formatPrice(signal.price)}</strong>
            <span>${escapeHtml(signal.timeframe || "-")} / ${escapeHtml(signal.strategy || "-")}</span>
          </div>
          <time>${formatSignalTime(signal)}</time>
        </div>
      `;
    })
    .join("");
}

function normalizeHistory(history) {
  return history
    .map((row) => ({
      time: row.time || row.date || row.tradingDate || row.trading_date || "",
      open: Number(row.open ?? row.Open ?? row.openPrice ?? row.o),
      high: Number(row.high ?? row.High ?? row.highPrice ?? row.h),
      low: Number(row.low ?? row.Low ?? row.lowPrice ?? row.l),
      close: Number(row.close ?? row.Close ?? row.closePrice ?? row.c),
      volume: Number(row.volume ?? row.Volume ?? row.v ?? 0),
    }))
    .filter((row) =>
      [row.open, row.high, row.low, row.close].every((value) => Number.isFinite(value))
    );
}

function normalizeMarkers(markers) {
  return markers
    .map((marker) => ({
      action: (marker.action || "").toLowerCase(),
      price: Number(marker.price),
      strategy: marker.strategy || "",
      time: marker.source_time || marker.received_at || "",
    }))
    .filter((marker) => ["buy", "sell"].includes(marker.action));
}

function drawCandles(rows, markers = []) {
  const canvas = els.canvas;
  const ctx = canvas.getContext("2d");
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.max(1, Math.floor(rect.width * dpr));
  canvas.height = Math.max(1, Math.floor(rect.height * dpr));
  ctx.scale(dpr, dpr);
  ctx.clearRect(0, 0, rect.width, rect.height);

  if (!rows.length) {
    clearChart(t("noHistory"));
    return;
  }

  const pad = { top: 22, right: 54, bottom: 28, left: 18 };
  const width = rect.width - pad.left - pad.right;
  const height = rect.height - pad.top - pad.bottom;
  const min = Math.min(...rows.map((row) => row.low));
  const max = Math.max(...rows.map((row) => row.high));
  const range = max - min || 1;
  const candleGap = width / rows.length;
  const bodyWidth = Math.max(4, Math.min(12, candleGap * 0.62));

  ctx.strokeStyle = cssVar("--line") || "#dbe2df";
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i += 1) {
    const y = pad.top + (height / 4) * i;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(rect.width - pad.right + 6, y);
    ctx.stroke();
    const label = max - (range / 4) * i;
    ctx.fillStyle = cssVar("--muted") || "#66727a";
    ctx.font = "12px system-ui";
    ctx.fillText(label.toFixed(2), rect.width - pad.right + 10, y + 4);
  }

  rows.forEach((row, index) => {
    const x = pad.left + candleGap * index + candleGap / 2;
    const yOpen = priceToY(row.open, min, range, pad.top, height);
    const yHigh = priceToY(row.high, min, range, pad.top, height);
    const yLow = priceToY(row.low, min, range, pad.top, height);
    const yClose = priceToY(row.close, min, range, pad.top, height);
    const up = row.close >= row.open;
    const color = up ? cssVar("--buy") || "#0f8f72" : cssVar("--sell") || "#c64242";

    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(x, yHigh);
    ctx.lineTo(x, yLow);
    ctx.stroke();

    const top = Math.min(yOpen, yClose);
    const bodyHeight = Math.max(2, Math.abs(yClose - yOpen));
    ctx.fillRect(x - bodyWidth / 2, top, bodyWidth, bodyHeight);
  });

  drawMarkers(ctx, rows, markers, {
    top: pad.top,
    height,
    min,
    range,
    candleGap,
    left: pad.left,
  });

  const last = rows[rows.length - 1];
  ctx.fillStyle = cssVar("--ink") || "#152025";
  ctx.font = "12px system-ui";
  ctx.fillText(String(last.time).slice(0, 10), pad.left, rect.height - 8);
}

function drawMarkers(ctx, rows, markers, scale) {
  if (!rows.length || !markers.length) return;

  const candleDates = rows.map((row) => normalizeDate(row.time));
  const candleTimes = rows.map((row) => Date.parse(row.time));

  markers.forEach((marker) => {
    const markerDate = normalizeDate(marker.time);
    let index = candleDates.indexOf(markerDate);
    if (index === -1) {
      index = nearestCandleIndex(candleTimes, Date.parse(marker.time));
    }
    if (index < 0) return;

    const candle = rows[index];
    const price = Number.isFinite(marker.price) && marker.price > 0
      ? marker.price
      : candle.close;
    const x = scale.left + scale.candleGap * index + scale.candleGap / 2;
    const y = priceToY(price, scale.min, scale.range, scale.top, scale.height);
    const isBuy = marker.action === "buy";
    const color = isBuy ? cssVar("--buy") || "#0f8f72" : cssVar("--sell") || "#c64242";
    const direction = isBuy ? 1 : -1;

    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(x, y - direction * 12);
    ctx.lineTo(x - 7, y - direction * 2);
    ctx.lineTo(x + 7, y - direction * 2);
    ctx.closePath();
    ctx.fill();
    ctx.font = "700 11px system-ui";
    ctx.fillText(isBuy ? "B" : "S", x - 4, y - direction * 16);
  });
}

function normalizeDate(value) {
  if (!value) return "";
  const parsed = new Date(value);
  if (!Number.isNaN(parsed.getTime())) {
    return parsed.toISOString().slice(0, 10);
  }
  return String(value).slice(0, 10);
}

function nearestCandleIndex(candleTimes, markerTime) {
  if (!Number.isFinite(markerTime)) return -1;
  let bestIndex = -1;
  let bestDistance = Number.POSITIVE_INFINITY;
  candleTimes.forEach((time, index) => {
    if (!Number.isFinite(time)) return;
    const distance = Math.abs(time - markerTime);
    if (distance < bestDistance) {
      bestIndex = index;
      bestDistance = distance;
    }
  });
  return bestIndex;
}

function clearChart(message) {
  const canvas = els.canvas;
  const ctx = canvas.getContext("2d");
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.max(1, Math.floor(rect.width * dpr));
  canvas.height = Math.max(1, Math.floor(rect.height * dpr));
  ctx.scale(dpr, dpr);
  ctx.clearRect(0, 0, rect.width, rect.height);
  ctx.fillStyle = cssVar("--muted") || "#66727a";
  ctx.font = "14px system-ui";
  ctx.fillText(message, 18, 38);
}

function priceToY(price, min, range, top, height) {
  return top + height - ((price - min) / range) * height;
}

function formatDate(value) {
  if (!value) return "-";
  const date = parseDateValue(value);
  if (!date) return value;
  return date.toLocaleString();
}

function signalTimeValue(signal) {
  return signal?.source_time || signal?.received_at || "";
}

function signalTimeSortValue(signal) {
  const parsed = parseDateValue(signalTimeValue(signal));
  return parsed ? parsed.getTime() : 0;
}

function formatSignalTime(signal) {
  return formatDate(signalTimeValue(signal));
}

function formatDateOnly(value) {
  if (!value) return "-";
  const raw = String(value);
  const isoDate = raw.match(/^\d{4}-\d{2}-\d{2}/)?.[0];
  if (!isoDate) return formatDate(value);
  const [year, month, day] = isoDate.split("-");
  return `${day}/${month}/${year}`;
}

function formatHoldingDaysBetween(startValue, endValue = null) {
  const start = parseDateValue(startValue);
  const end = endValue ? parseDateValue(endValue) : new Date();
  if (!start || !end) return "-";
  const dayMs = 24 * 60 * 60 * 1000;
  const days = Math.max(0, Math.floor((end.getTime() - start.getTime()) / dayMs));
  return `${days}d`;
}

function parseDateValue(value) {
  if (!value) return null;
  const raw = String(value);
  const dateOnly = raw.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (dateOnly) {
    return new Date(Number(dateOnly[1]), Number(dateOnly[2]) - 1, Number(dateOnly[3]));
  }
  const pineIso = raw.match(/^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})$/);
  if (pineIso) {
    return new Date(`${pineIso[1]}T${pineIso[2]}`);
  }
  const slashDateTime = raw.match(
    /^(\d{1,2})\/(\d{1,2})\/(\d{4}),?\s+(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(AM|PM)$/i
  );
  if (slashDateTime) {
    const month = Number(slashDateTime[1]);
    const day = Number(slashDateTime[2]);
    const year = Number(slashDateTime[3]);
    let hour = Number(slashDateTime[4]);
    const minute = Number(slashDateTime[5]);
    const second = Number(slashDateTime[6] || 0);
    const meridiem = slashDateTime[7].toUpperCase();
    if (meridiem === "PM" && hour < 12) hour += 12;
    if (meridiem === "AM" && hour === 12) hour = 0;
    return new Date(year, month - 1, day, hour, minute, second);
  }
  const parsed = new Date(raw);
  return Number.isNaN(parsed.getTime()) ? null : parsed;
}

function formatPrice(value) {
  if (value === null || value === undefined) return "-";
  return Number(value).toLocaleString(undefined, {
    maximumFractionDigits: 3,
  });
}

function rawNumber(value) {
  if (value === null || value === undefined) return "";
  const number = Number(value);
  return Number.isFinite(number) ? String(number) : "";
}

function optionalNumber(value) {
  if (value === null || value === undefined || value === "") return null;
  const number = parsePriceInput(value);
  return Number.isFinite(number) ? number : null;
}

function parsePriceInput(value) {
  return Number(String(value).trim().replaceAll(",", ""));
}

function localDateToIsoDate(value) {
  if (!value) return null;
  return /^\d{4}-\d{2}-\d{2}$/.test(value) ? value : null;
}

function formatDuration(seconds) {
  if (seconds === null || seconds === undefined) return "-";
  const totalMinutes = Math.floor(Number(seconds) / 60);
  const days = Math.floor(totalMinutes / 1440);
  const hours = Math.floor((totalMinutes % 1440) / 60);
  const minutes = totalMinutes % 60;
  const parts = [];
  if (days) parts.push(`${days}d`);
  if (hours) parts.push(`${hours}h`);
  if (minutes || !parts.length) parts.push(`${minutes}m`);
  return parts.join(" ");
}

function formatPercent(value) {
  if (value === null || value === undefined) return "-";
  return `${Number(value).toFixed(1)}%`;
}

function formatSignedPercent(value) {
  if (value === null || value === undefined) return "-";
  const number = Number(value);
  const className = number >= 0 ? "positive" : "negative";
  const sign = number > 0 ? "+" : "";
  return `<span class="${className}">${sign}${number.toFixed(2)}%</span>`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

els.refresh.addEventListener("click", refresh);
els.languageSelect.value = state.language;
els.languageSelect.addEventListener("change", async () => {
  state.language = els.languageSelect.value;
  localStorage.setItem("dashboardLanguage", state.language);
  applyTranslations();
  await refresh();
});
els.themeToggle.addEventListener("click", () => {
  state.theme = state.theme === "dark" ? "light" : "dark";
  localStorage.setItem("dashboardTheme", state.theme);
  applyTheme();
});
els.tabButtons.forEach((button) => {
  button.addEventListener("click", () => setActiveTab(button.dataset.tabTarget));
});
els.watchlistInput.addEventListener("change", updateWatchlistFromInput);
els.watchlistInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") updateWatchlistFromInput();
});
els.watchlistOnly.addEventListener("change", toggleWatchlistOnly);
els.addTickerToWatchlist.addEventListener("click", addSelectedTickerToWatchlist);
els.openPositionTickerFilter.addEventListener("input", renderOpenPositions);
els.openPositionStrategyFilter.addEventListener("input", renderOpenPositions);
els.openPositionSort.addEventListener("change", renderOpenPositions);
els.openPositionRefreshPrices.addEventListener("click", refreshOpenPositionMarketPrices);
els.performanceTickerFilter.addEventListener("input", refresh);
els.performanceStrategyFilter.addEventListener("input", refresh);
els.performanceSort.addEventListener("change", refresh);
els.clearClosedTradesFilter.addEventListener("click", clearClosedTradeFilter);
els.manualPositionForm.addEventListener("submit", addManualPosition);
els.manualRefreshPrices.addEventListener("click", refreshManualMarketPrices);
window.addEventListener("resize", () => {
  if (state.selectedTicker) renderChart(state.selectedTicker);
  if (state.activeTab === "manualPortfolio") {
    drawManualEquityCurve(state.manualPortfolio.equity_curve || []);
  }
});

applyTheme();
applyTranslations();
updateWatchlistControls();
setActiveTab(state.activeTab);
refresh();
setInterval(refresh, 15000);
