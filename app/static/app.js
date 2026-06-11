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
  manualDailyPerformanceTable: document.querySelector("#manualDailyPerformanceTable"),
  manualPositionForm: document.querySelector("#manualPositionForm"),
  manualTicker: document.querySelector("#manualTicker"),
  manualWeight: document.querySelector("#manualWeight"),
  manualEntryPrice: document.querySelector("#manualEntryPrice"),
  manualCurrentPrice: document.querySelector("#manualCurrentPrice"),
  manualQuantity: document.querySelector("#manualQuantity"),
  manualEntryDate: document.querySelector("#manualEntryDate"),
  manualNote: document.querySelector("#manualNote"),
  manualPortfolioReturn: document.querySelector("#manualPortfolioReturn"),
  manualRecordDailyPerformance: document.querySelector("#manualRecordDailyPerformance"),
  manualDailyPerformanceStatus: document.querySelector("#manualDailyPerformanceStatus"),
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
  openPositionsTotalReturn: document.querySelector("#openPositionsTotalReturn"),
  openPositionTickerFilter: document.querySelector("#openPositionTickerFilter"),
  openPositionStrategyFilter: document.querySelector("#openPositionStrategyFilter"),
  openPositionConfirmFilter: document.querySelector("#openPositionConfirmFilter"),
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
  chart: document.querySelector("#priceChart"),
  chartEmpty: document.querySelector("#priceChartEmpty"),
  equityCanvas: document.querySelector("#equityChart"),
  manualEquityCanvas: document.querySelector("#manualEquityChart"),
  dividendEventForm: document.querySelector("#dividendEventForm"),
  dividendTicker: document.querySelector("#dividendTicker"),
  dividendExDate: document.querySelector("#dividendExDate"),
  dividendCashAmount: document.querySelector("#dividendCashAmount"),
  dividendStockRatio: document.querySelector("#dividendStockRatio"),
  dividendIssueRatio: document.querySelector("#dividendIssueRatio"),
  dividendIssuePrice: document.querySelector("#dividendIssuePrice"),
  dividendNote: document.querySelector("#dividendNote"),
  dividendEventsTable: document.querySelector("#dividendEventsTable"),
  exDateAlerts: document.querySelector("#exDateAlerts"),
  derivativeOpenCount: document.querySelector("#derivativeOpenCount"),
  derivativeOpenPnl: document.querySelector("#derivativeOpenPnl"),
  derivativeClosedCount: document.querySelector("#derivativeClosedCount"),
  derivativeRealizedPnl: document.querySelector("#derivativeRealizedPnl"),
  derivativeInitialCapital: document.querySelector("#derivativeInitialCapital"),
  derivativeCurrentEquity: document.querySelector("#derivativeCurrentEquity"),
  derivativeMaxDrawdown: document.querySelector("#derivativeMaxDrawdown"),
  derivativeMaxDrawdownPct: document.querySelector("#derivativeMaxDrawdownPct"),
  derivativeTotalPnl: document.querySelector("#derivativeTotalPnl"),
  derivativeTotalReturn: document.querySelector("#derivativeTotalReturn"),
  derivativeWinningTrades: document.querySelector("#derivativeWinningTrades"),
  derivativeProfitFactor: document.querySelector("#derivativeProfitFactor"),
  derivativeEquityCanvas: document.querySelector("#derivativeEquityChart"),
  derivativeCapitalForm: document.querySelector("#derivativeCapitalForm"),
  derivativeCapitalInput: document.querySelector("#derivativeCapitalInput"),
  derivativeOpenPositionsTable: document.querySelector("#derivativeOpenPositionsTable"),
  derivativeClosedTradesTable: document.querySelector("#derivativeClosedTradesTable"),
  derivativeEventsTable: document.querySelector("#derivativeEventsTable"),
  loginScreen: document.querySelector("#loginScreen"),
  loginForm: document.querySelector("#loginForm"),
  loginUsername: document.querySelector("#loginUsername"),
  loginPassword: document.querySelector("#loginPassword"),
  loginError: document.querySelector("#loginError"),
  currentUser: document.querySelector("#currentUser"),
  logoutButton: document.querySelector("#logoutButton"),
  userCreateForm: document.querySelector("#userCreateForm"),
  newUsername: document.querySelector("#newUsername"),
  newPassword: document.querySelector("#newPassword"),
  newUserRole: document.querySelector("#newUserRole"),
  newUserFeatures: document.querySelector("#newUserFeatures"),
  usersTable: document.querySelector("#usersTable"),
};

const FALLBACK_SIGNAL_WEIGHT_PCT = 5;
const FEATURE_LABELS = {
  overview: "Tổng quan",
  positions: "Vị thế",
  derivatives: "Phái sinh VN30",
  manualPortfolio: "Danh mục tay",
  performance: "Hiệu suất",
  dividends: "Cổ tức",
  logs: "Nhật ký",
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
    tabDerivatives: "VN30 Derivatives",
    tabManualPortfolio: "Manual Portfolio",
    tabPerformance: "Performance",
    tabDividends: "Dividends",
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
    action: "Action",
    strategyPerformance: "Strategy Performance",
    buyToSellResults: "Buy to Sell Results",
    closed: "Closed",
    open: "Open",
    winRate: "Win Rate",
    realized: "Realized",
    realizedPl: "Realized P/L",
    openPl: "Open P/L",
    current: "Current",
    currentPl: "Current P/L",
    openUnrealizedPl: "Unrealized P/L",
    allocationWeight: "Weight",
    portfolioPl: "P/L",
    confirm: "Signal",
    confirmAll: "All signal states",
    confirmedOnly: "Has other signal",
    unconfirmedOnly: "No other signal",
    confirmedStatus: "Has other signal",
    unconfirmedStatus: "No other signal",
    noConfirmations: "No other signal",
    confirmBuyTitle: "Other signal received",
    dailyPerformance: "Daily Performance",
    savedDailyPerformance: "Saved Daily Performance",
    date: "Date",
    equityValue: "Equity",
    savedAt: "Saved At",
    noDailyPerformance: "No saved daily performance",
    deleteDailyPerformanceConfirm: "Delete this saved daily performance record?",
    deleteDailyPerformanceFailed: "Could not delete saved daily performance",
    confirmationStats: "Signal Stats",
    confirmVsNoConfirm: "Other Signal vs None",
    avgReturn: "Avg Return",
    totalReturn: "Total Return",
    exportBackup: "Export / Backup",
    downloadData: "Download Data",
    exportSignals: "Signals CSV",
    exportManualPortfolio: "Manual CSV",
    exportDailyPerformance: "Daily CSV",
    exportDividends: "Dividends CSV",
    exportDerivatives: "Derivatives CSV",
    backupDatabase: "Backup DB",
    dividendCalendar: "Dividend Calendar",
    dividendRules: "Ex-rights Adjustments",
    dividend: "Dividend",
    exDate: "Ex-date",
    cashDividend: "Cash",
    stockDividend: "Stock %",
    additionalIssue: "Issue %",
    issuePrice: "Issue Price",
    addDividendEvent: "Add event",
    noDividendEvents: "No dividend events",
    noDividends: "No dividend events",
    upcomingDividend: "Upcoming",
    appliedDividend: "Adjusted",
    dividendDeleteConfirm: "Delete this dividend event?",
    dividendSaveFailed: "Could not save dividend event",
    dividendDeleteFailed: "Could not delete dividend event",
    exDateToday: "Ex-date today",
    exDateAlertMessage: "Ex-rights date today for open positions",
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
    recordDailyPerformance: "Save EOD",
    dailyPerformanceEmpty: "No saved daily performance yet",
    dailyPerformanceStatus: "Saved days",
    dailyPerformanceLatest: "Latest",
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
    baseStrategyNotOpen: "Base strategy is not open",
    noSignals: "No signals yet",
    noTimeline: "No timeline for this ticker",
    noHistory: "No price history available",
    delete: "Delete",
    deleteTitle: "Delete signal",
    deleteConfirm: "Delete this signal?",
    deleteFailed: "Could not delete signal",
    reopenPosition: "Reopen",
    reopenPositionTitle: "Reopen position",
    reopenPositionConfirm: "Delete the closing sell signal and reopen this position?",
    reopenPositionFailed: "Could not reopen position",
    performanceTickerPlaceholder: "Ticker",
    performanceStrategyPlaceholder: "Strategy",
    openPositionTickerPlaceholder: "Ticker",
    openPositionStrategyPlaceholder: "Strategy",
    vn30Derivatives: "VN30 Derivatives",
    derivativeOpenPositions: "Open Positions",
    derivativeOpenPnl: "Open P/L",
    derivativeClosedTrades: "Closed Trades",
    derivativeRealizedPnl: "Realized P/L",
    derivativeInitialCapital: "Initial Capital",
    derivativeCurrentEquity: "Current Equity",
    derivativeMaxDrawdown: "Maximum Equity Drawdown",
    derivativeMaxDrawdownPct: "Maximum Equity Drawdown %",
    derivativeTotalPnl: "Total P/L",
    derivativeTotalReturn: "Total Return",
    derivativeWinningTrades: "Winning Trades",
    derivativeProfitFactor: "Profit Factor",
    derivativePerformance: "Derivative Performance",
    derivativeEquityCurve: "Equity and Maximum Drawdown",
    derivativeCapitalPlaceholder: "Initial capital (VND)",
    saveCapital: "Save capital",
    derivativeCapitalSaveFailed: "Could not save derivative capital",
    derivativeCurrentPositions: "Current Long / Short Positions",
    derivativeTradeHistory: "Derivative Trade History",
    derivativeEvents: "Derivative Events",
    derivativeWebhookHistory: "Webhook Event History",
    averagePrice: "Average Price",
    contracts: "Contracts",
    layers: "Layers",
    pnlPoints: "P/L Points",
    pnlVnd: "P/L VND",
    noDerivativePositions: "No open derivative positions",
    noDerivativeTrades: "No closed derivative trades",
    noDerivativeEvents: "No derivative events",
    deleteDerivativeConfirm: "Delete this derivative event?",
    deleteDerivativeFailed: "Could not delete derivative event",
  },
  vi: {
    webhookLabel: "Webhook TradingView",
    refresh: "Làm mới",
    darkMode: "Chế độ tối",
    lightMode: "Chế độ sáng",
    watchlistOnly: "Chỉ watchlist",
    addToWatchlist: "Thêm vào watchlist",
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
    action: "Thao tác",
    strategyPerformance: "Hiệu suất chiến lược",
    buyToSellResults: "Kết quả Mua đến Bán",
    closed: "Đã đóng",
    open: "Đang mở",
    winRate: "Tỷ lệ thắng",
    realized: "Đã chốt",
    realizedPl: "Lãi/lỗ đã chốt",
    openPl: "Lãi/lỗ mở",
    current: "Hiện tại",
    currentPl: "Lãi/lỗ hiện tại",
    openUnrealizedPl: "Lãi/lỗ tạm tính",
    allocationWeight: "Tỷ trọng",
    portfolioPl: "Lãi/lỗ",
    confirmAll: "Tất cả xác nhận",
    confirmedOnly: "Đã xác nhận",
    unconfirmedOnly: "Chưa xác nhận",
    confirmedStatus: "Đã xác nhận",
    unconfirmedStatus: "Chưa xác nhận",
    noConfirmations: "Chưa có xác nhận",
    dailyPerformance: "Hiệu suất ngày",
    savedDailyPerformance: "Hiệu suất ngày đã lưu",
    date: "Ngày",
    equityValue: "Vốn",
    savedAt: "Lúc lưu",
    noDailyPerformance: "Chưa có hiệu suất ngày đã lưu",
    confirmationStats: "Thống kê xác nhận",
    confirmVsNoConfirm: "Có xác nhận vs chưa xác nhận",
    avgReturn: "Lãi/lỗ TB",
    totalReturn: "Tổng lãi/lỗ",
    exportBackup: "Xuất / Sao lưu",
    downloadData: "Tải dữ liệu",
    exportSignals: "Tín hiệu CSV",
    exportManualPortfolio: "Danh mục CSV",
    exportDailyPerformance: "Hiệu suất ngày CSV",
    backupDatabase: "Sao lưu DB",
    baseStrategyNotOpen: "Chiến lược gốc chưa mở",
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
    openUnrealizedPl: "Lãi/lỗ tạm tính (5%/mã)",
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
    recordDailyPerformance: "Lưu cuối ngày",
    dailyPerformanceEmpty: "Chưa có hiệu suất ngày đã lưu",
    dailyPerformanceStatus: "Số ngày đã lưu",
    dailyPerformanceLatest: "Gần nhất",
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
    reopenPosition: "Mở lại",
    reopenPositionTitle: "Mở lại vị thế",
    reopenPositionConfirm: "Xóa tín hiệu Sell đã đóng lệnh và đưa vị thế này trở lại đang nắm?",
    reopenPositionFailed: "Không thể mở lại vị thế",
    performanceTickerPlaceholder: "Mã",
    performanceStrategyPlaceholder: "Chiến lược",
    openPositionTickerPlaceholder: "Mã",
    openPositionStrategyPlaceholder: "Chiến lược",
  },
};

Object.assign(translations.vi, {
  webhookLabel: "Webhook TradingView",
  refresh: "Làm mới",
  darkMode: "Chế độ tối",
  lightMode: "Chế độ sáng",
  watchlistOnly: "Chỉ watchlist",
  addToWatchlist: "Thêm vào watchlist",
  tickerTimeline: "Timeline mã",
  clearFilter: "Xóa lọc",
  filteredTrades: "Đang xem giao dịch của",
  tabOverview: "Tổng quan",
  tabPositions: "Vị thế",
  tabManualPortfolio: "Danh mục tay",
  tabPerformance: "Hiệu suất",
  tabDividends: "Cổ tức",
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
  realizedPl: "Lãi/lỗ đã chốt",
  openPl: "Lãi/lỗ mở",
  current: "Hiện tại",
  currentPl: "Lãi/lỗ hiện tại",
  openUnrealizedPl: "Lãi/lỗ tạm tính",
  allocationWeight: "Tỷ trọng",
  portfolioPl: "Lãi/lỗ",
  confirm: "Tín hiệu",
  confirmAll: "Tất cả trạng thái tín hiệu",
  confirmedOnly: "Có tín hiệu khác",
  unconfirmedOnly: "Chưa có tín hiệu khác",
  confirmedStatus: "Có tín hiệu khác",
  unconfirmedStatus: "Chưa có tín hiệu khác",
  noConfirmations: "Chưa có tín hiệu khác",
  confirmBuyTitle: "Đã có tín hiệu khác",
  dailyPerformance: "Hiệu suất ngày",
  savedDailyPerformance: "Hiệu suất ngày đã lưu",
  date: "Ngày",
  equityValue: "Vốn",
  savedAt: "Lúc lưu",
  noDailyPerformance: "Chưa có hiệu suất ngày đã lưu",
  deleteDailyPerformanceConfirm: "Xóa bản ghi hiệu suất ngày này?",
  deleteDailyPerformanceFailed: "Không thể xóa hiệu suất ngày đã lưu",
  confirmationStats: "Thống kê tín hiệu",
  confirmVsNoConfirm: "Có tín hiệu khác vs chưa có",
  avgReturn: "Lãi/lỗ TB",
  totalReturn: "Tổng lãi/lỗ",
  exportBackup: "Xuất / Sao lưu",
  downloadData: "Tải dữ liệu",
  exportSignals: "Tín hiệu CSV",
  exportManualPortfolio: "Danh mục CSV",
  exportDailyPerformance: "Hiệu suất ngày CSV",
  exportDividends: "Cổ tức CSV",
  backupDatabase: "Sao lưu DB",
  dividendCalendar: "Lịch cổ tức",
  dividendRules: "Điều chỉnh ngày GDKHQ",
  dividend: "Cổ tức",
  exDate: "Ngày GDKHQ",
  cashDividend: "Tiền mặt",
  stockDividend: "Cổ phiếu %",
  additionalIssue: "Phát hành thêm %",
  issuePrice: "Giá phát hành",
  addDividendEvent: "Thêm sự kiện",
  noDividendEvents: "Chưa có lịch cổ tức",
  noDividends: "Không có cổ tức",
  upcomingDividend: "Sắp tới",
  appliedDividend: "Đã điều chỉnh",
  dividendDeleteConfirm: "Xóa sự kiện cổ tức này?",
  dividendSaveFailed: "Không thể lưu sự kiện cổ tức",
  dividendDeleteFailed: "Không thể xóa sự kiện cổ tức",
  exDateToday: "Hôm nay là ngày GDKHQ",
  exDateAlertMessage: "Cảnh báo ngày giao dịch không hưởng quyền cho vị thế đang mở",
  baseStrategyNotOpen: "Chiến lược gốc chưa mở",
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
  recordDailyPerformance: "Lưu cuối ngày",
  dailyPerformanceEmpty: "Chưa có hiệu suất ngày đã lưu",
  dailyPerformanceStatus: "Số ngày đã lưu",
  dailyPerformanceLatest: "Gần nhất",
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
  tabDerivatives: "Phái sinh VN30",
  exportDerivatives: "Phái sinh CSV",
  vn30Derivatives: "Phái sinh VN30",
  derivativeOpenPositions: "Vị thế đang mở",
  derivativeOpenPnl: "Lãi/lỗ tạm tính",
  derivativeClosedTrades: "Lệnh đã đóng",
  derivativeRealizedPnl: "Lãi/lỗ đã chốt",
  derivativeInitialCapital: "Vốn ban đầu",
  derivativeCurrentEquity: "Vốn hiện tại",
  derivativeMaxDrawdown: "Mức giảm vốn chủ sở hữu lớn nhất",
  derivativeMaxDrawdownPct: "Mức giảm vốn chủ sở hữu lớn nhất %",
  derivativeTotalPnl: "Tổng lãi/lỗ",
  derivativeTotalReturn: "Tỷ suất tổng",
  derivativeWinningTrades: "Giao dịch lãi",
  derivativeProfitFactor: "Hệ số lợi nhuận",
  derivativePerformance: "Hiệu suất phái sinh",
  derivativeEquityCurve: "Vốn chủ sở hữu và mức sụt giảm tối đa",
  derivativeCapitalPlaceholder: "Vốn ban đầu (VND)",
  saveCapital: "Lưu vốn",
  derivativeCapitalSaveFailed: "Không thể lưu vốn phái sinh",
  derivativeCurrentPositions: "Vị thế Long / Short hiện tại",
  derivativeTradeHistory: "Lịch sử giao dịch phái sinh",
  derivativeEvents: "Sự kiện phái sinh",
  derivativeWebhookHistory: "Lịch sử webhook phái sinh",
  averagePrice: "Giá vốn",
  contracts: "Hợp đồng",
  layers: "Số lớp",
  pnlPoints: "Lãi/lỗ điểm",
  pnlVnd: "Lãi/lỗ VND",
  noDerivativePositions: "Không có vị thế phái sinh đang mở",
  noDerivativeTrades: "Chưa có lệnh phái sinh đã đóng",
  noDerivativeEvents: "Chưa có sự kiện phái sinh",
  deleteDerivativeConfirm: "Xóa sự kiện phái sinh này?",
  deleteDerivativeFailed: "Không thể xóa sự kiện phái sinh",
});

const state = {
  user: null,
  availableFeatures: Object.keys(FEATURE_LABELS),
  users: [],
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
  defaultSignalWeightPct: FALLBACK_SIGNAL_WEIGHT_PCT,
  manualPortfolio: { positions: [], equity_curve: [], summary: {} },
  dividendEvents: [],
  derivatives: { summary: {}, open_positions: [], closed_trades: [], events: [] },
};

const priceChartState = {
  chart: null,
  candleSeries: null,
  volumeSeries: null,
  markerPlugin: null,
  resizeObserver: null,
  ticker: "",
  requestId: 0,
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

function allocatedReturnPct(returnPct) {
  const value = Number(returnPct);
  return Number.isFinite(value)
    ? (value * state.defaultSignalWeightPct) / 100
    : null;
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
  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    element.placeholder = t(element.dataset.i18nPlaceholder);
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
  if (priceChartState.chart) {
    applyPriceChartTheme();
  } else if (state.selectedTicker) {
    renderChart(state.selectedTicker);
  }
  if (state.activeTab === "performance") {
    drawEquityCurve(state.closedTrades);
  }
  if (state.activeTab === "manualPortfolio") {
    drawManualEquityCurve(state.manualPortfolio.equity_curve || []);
  }
  if (state.activeTab === "derivatives") {
    drawDerivativeEquityCurve(state.derivatives.equity_curve || []);
  }
}

function updateThemeButton() {
  const isDark = state.theme === "dark";
  els.themeToggle.textContent = isDark ? t("lightMode") : t("darkMode");
  els.themeToggle.title = isDark ? t("lightMode") : t("darkMode");
}

function setActiveTab(tabName) {
  const exists = [...els.tabButtons].some(
    (button) =>
      button.dataset.tabTarget === tabName && button.dataset.accessHidden !== "true"
  );
  if (!exists) {
    tabName =
      [...els.tabButtons].find((button) => button.dataset.accessHidden !== "true")
        ?.dataset.tabTarget || "overview";
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
  if (tabName === "derivatives") {
    drawDerivativeEquityCurve(state.derivatives.equity_curve || []);
  }
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (response.status === 401) {
    showLogin();
  }
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return response.json();
}

function featureEnabled(feature) {
  if (!state.user) return false;
  if (state.user.role === "admin") return true;
  const required = Array.isArray(feature) ? feature : [feature];
  return required.some((item) => state.user.features.includes(item));
}

function featureFetch(feature, url, fallback) {
  return featureEnabled(feature) ? fetchJson(url) : Promise.resolve(fallback);
}

async function bootstrapAuth() {
  try {
    const payload = await fetchJson("/api/auth/me");
    if (!payload.user) {
      showLogin();
      return;
    }
    setAuthenticatedUser(payload.user, payload.available_features || []);
    await refresh();
  } catch (error) {
    showLogin();
  }
}

function setAuthenticatedUser(user, availableFeatures) {
  state.user = user;
  state.availableFeatures = availableFeatures.length ? availableFeatures : Object.keys(FEATURE_LABELS);
  els.loginScreen.hidden = true;
  els.currentUser.textContent = `${user.username} · ${user.role}`;
  document.body.classList.toggle("readOnly", user.role !== "admin");
  applyAccessControl();
  if (user.role === "admin") {
    renderFeatureSelector(els.newUserFeatures, state.availableFeatures);
    loadAdminUsers();
  }
}

function showLogin() {
  state.user = null;
  els.loginScreen.hidden = false;
  els.loginPassword.value = "";
  els.loginUsername.focus();
}

async function submitLogin(event) {
  event.preventDefault();
  els.loginError.hidden = true;
  const response = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: els.loginUsername.value.trim(),
      password: els.loginPassword.value,
    }),
  });
  if (!response.ok) {
    els.loginError.textContent = "Sai tài khoản hoặc mật khẩu";
    els.loginError.hidden = false;
    return;
  }
  const payload = await response.json();
  const me = await fetchJson("/api/auth/me");
  setAuthenticatedUser(payload.user, me.available_features || []);
  await refresh();
}

async function logout() {
  await fetch("/api/auth/logout", { method: "POST" });
  showLogin();
}

function applyAccessControl() {
  const allowed = new Set(state.user?.features || []);
  const isAdmin = state.user?.role === "admin";
  document.querySelectorAll("[data-tab-target]").forEach((button) => {
    const target = button.dataset.tabTarget;
    const visible = target === "admin" ? isAdmin : isAdmin || allowed.has(target);
    button.dataset.accessHidden = visible ? "false" : "true";
  });
  document.querySelectorAll("[data-tab-panel]").forEach((panel) => {
    const target = panel.dataset.tabPanel;
    const visible = target === "admin" ? isAdmin : isAdmin || allowed.has(target);
    panel.dataset.accessHidden = visible ? "false" : "true";
  });
  [
    els.openPositionRefreshPrices,
    els.manualPositionForm,
    els.manualRefreshPrices,
    els.manualRecordDailyPerformance,
    els.dividendEventForm,
    els.derivativeCapitalForm,
    document.querySelector(".exportActions"),
  ].forEach((element) => element?.classList.add("adminOnly"));
  setActiveTab(state.activeTab);
}

function renderFeatureSelector(container, selectedFeatures = []) {
  const selected = new Set(selectedFeatures);
  container.innerHTML = state.availableFeatures
    .map((feature) => `
      <label class="featureOption">
        <input type="checkbox" value="${escapeHtml(feature)}" ${selected.has(feature) ? "checked" : ""} />
        <span>${escapeHtml(FEATURE_LABELS[feature] || feature)}</span>
      </label>
    `)
    .join("");
}

function selectedFeatures(container) {
  return [...container.querySelectorAll('input[type="checkbox"]:checked')].map(
    (input) => input.value
  );
}

async function loadAdminUsers() {
  if (state.user?.role !== "admin") return;
  const payload = await fetchJson("/api/admin/users");
  state.users = payload.users || [];
  state.availableFeatures = payload.available_features || state.availableFeatures;
  renderAdminUsers();
}

function renderAdminUsers() {
  els.usersTable.innerHTML = state.users
    .map((user) => `
      <tr data-user-id="${user.id}">
        <td><strong>${escapeHtml(user.username)}</strong></td>
        <td>
          <select data-user-role>
            <option value="user" ${user.role === "user" ? "selected" : ""}>User chỉ xem</option>
            <option value="admin" ${user.role === "admin" ? "selected" : ""}>Admin</option>
          </select>
        </td>
        <td><div class="featureSelector" data-user-features></div></td>
        <td>
          <label class="featureOption">
            <input data-user-active type="checkbox" ${user.active ? "checked" : ""} />
            <span>Hoạt động</span>
          </label>
        </td>
        <td><input data-user-password type="password" minlength="8" placeholder="Để trống nếu giữ nguyên" /></td>
        <td>
          <button class="smallButton" type="button" data-user-save>Lưu</button>
          ${user.id === state.user.id ? "" : `<button class="deleteButton" type="button" data-user-delete>Xóa</button>`}
        </td>
      </tr>
    `)
    .join("");

  state.users.forEach((user) => {
    const row = els.usersTable.querySelector(`[data-user-id="${user.id}"]`);
    renderFeatureSelector(row.querySelector("[data-user-features]"), user.features);
    row.querySelector("[data-user-save]").addEventListener("click", () => saveAdminUser(user.id));
    row.querySelector("[data-user-delete]")?.addEventListener("click", () => deleteAdminUser(user.id));
  });
}

async function createAdminUser(event) {
  event.preventDefault();
  const response = await fetch("/api/admin/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: els.newUsername.value.trim(),
      password: els.newPassword.value,
      role: els.newUserRole.value,
      features: selectedFeatures(els.newUserFeatures),
    }),
  });
  if (!response.ok) {
    window.alert((await response.json()).detail || "Không thể tạo tài khoản");
    return;
  }
  els.userCreateForm.reset();
  renderFeatureSelector(els.newUserFeatures, state.availableFeatures);
  await loadAdminUsers();
}

async function saveAdminUser(userId) {
  const row = els.usersTable.querySelector(`[data-user-id="${userId}"]`);
  const password = row.querySelector("[data-user-password]").value;
  const body = {
    role: row.querySelector("[data-user-role]").value,
    active: row.querySelector("[data-user-active]").checked,
    features: selectedFeatures(row.querySelector("[data-user-features]")),
  };
  if (password) body.password = password;
  const response = await fetch(`/api/admin/users/${userId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    window.alert((await response.json()).detail || "Không thể cập nhật tài khoản");
    return;
  }
  await loadAdminUsers();
}

async function deleteAdminUser(userId) {
  if (!window.confirm("Xóa tài khoản này?")) return;
  const response = await fetch(`/api/admin/users/${userId}`, { method: "DELETE" });
  if (!response.ok) {
    window.alert((await response.json()).detail || "Không thể xóa tài khoản");
    return;
  }
  await loadAdminUsers();
}

function settledPayload(result, fallback, label) {
  if (result.status === "fulfilled") {
    return result.value;
  }
  console.error(`Failed to load ${label}`, result.reason);
  return fallback;
}

async function refresh() {
  if (!state.user) return;
  const query = "";
  const performanceQuery = buildPerformanceQuery();
  const results = await Promise.allSettled([
    fetchJson("/api/settings"),
    featureFetch("overview", "/api/summary", { total: 0, buy_count: 0, sell_count: 0, tickers: 0 }),
    featureFetch("overview", `/api/signals${query}`, { signals: [] }),
    featureFetch(["positions", "performance"], `/api/performance${performanceQuery}`, {
      open_trades: [],
      closed_trades: [],
      strategies: [],
      ignored_signals: [],
    }),
    featureFetch("logs", "/api/invalid-signals", { invalid_signals: [] }),
    featureFetch("manualPortfolio", "/api/manual-portfolio", state.manualPortfolio),
    featureFetch("dividends", "/api/dividend-events", { dividend_events: [] }),
    featureFetch("derivatives", "/api/derivatives", state.derivatives),
  ]);

  const settingsPayload = settledPayload(
    results[0],
    { default_signal_weight_pct: state.defaultSignalWeightPct },
    "settings"
  );
  const summary = settledPayload(
    results[1],
    { total: 0, buy_count: 0, sell_count: 0, tickers: 0, latest_received_at: null },
    "summary"
  );
  const signalsPayload = settledPayload(results[2], { signals: state.signals }, "signals");
  const performancePayload = settledPayload(
    results[3],
    {
      open_trades: state.openTrades,
      closed_trades: state.closedTrades,
      strategies: [],
      ignored_signals: [],
    },
    "performance"
  );
  const invalidPayload = settledPayload(results[4], { invalid_signals: [] }, "invalid signals");
  const manualPayload = settledPayload(results[5], state.manualPortfolio, "manual portfolio");
  const dividendPayload = settledPayload(
    results[6],
    { dividend_events: state.dividendEvents },
    "dividend events"
  );
  const derivativePayload = settledPayload(
    results[7],
    state.derivatives,
    "derivatives"
  );

  state.defaultSignalWeightPct = Number(settingsPayload.default_signal_weight_pct) || FALLBACK_SIGNAL_WEIGHT_PCT;
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
  state.dividendEvents = dividendPayload.dividend_events || [];
  renderDividendEvents();
  renderExDateAlerts();
  state.derivatives = derivativePayload;
  renderDerivatives(derivativePayload);

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
  renderManualDailyPerformanceStatus(payload.daily_performance || []);
  renderManualDailyPerformanceTable(payload.daily_performance || []);
  drawManualEquityCurve(payload.equity_curve || []);

  if (!positions.length) {
    els.manualPortfolioTable.innerHTML = `<tr><td class="empty" colspan="12">${t("noManualPositions")}</td></tr>`;
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
          <td>${renderDividendNotes(position.dividend_notes || [])}</td>
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

function renderManualDailyPerformanceStatus(dailyPerformance) {
  if (!dailyPerformance.length) {
    els.manualDailyPerformanceStatus.textContent = t("dailyPerformanceEmpty");
    return;
  }
  const latest = dailyPerformance[dailyPerformance.length - 1];
  els.manualDailyPerformanceStatus.innerHTML = `
    <span>${escapeHtml(t("dailyPerformanceStatus"))}: <strong>${dailyPerformance.length}</strong></span>
    <span>${escapeHtml(t("dailyPerformanceLatest"))}: <strong>${escapeHtml(formatDateOnly(latest.trade_date || latest.recorded_at))}</strong></span>
    <span>${escapeHtml(t("returnPct"))}: ${formatSignedPercent(latest.portfolio_return_pct)}</span>
  `;
}

function renderManualDailyPerformanceTable(dailyPerformance) {
  const rows = [...dailyPerformance].reverse();
  if (!rows.length) {
    els.manualDailyPerformanceTable.innerHTML = `<tr><td class="empty" colspan="8">${t("noDailyPerformance")}</td></tr>`;
    return;
  }
  els.manualDailyPerformanceTable.innerHTML = rows
    .map((row) => `
      <tr>
        <td>${formatDateOnly(row.trade_date)}</td>
        <td>${formatSignedPercent(row.portfolio_return_pct)}</td>
        <td>${formatPrice(row.equity_value)}</td>
        <td>${formatPercent(row.total_weight_pct)}</td>
        <td>${row.open_count ?? 0}</td>
        <td>${row.closed_count ?? 0}</td>
        <td>${formatDate(row.recorded_at)}</td>
        <td>
          <button class="deleteButton" type="button" data-daily-performance-delete="${escapeHtml(row.trade_date)}">${escapeHtml(t("delete"))}</button>
        </td>
      </tr>
    `)
    .join("");

  els.manualDailyPerformanceTable
    .querySelectorAll("[data-daily-performance-delete]")
    .forEach((button) => {
      button.addEventListener("click", () =>
        deleteManualDailyPerformance(button.dataset.dailyPerformanceDelete)
      );
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

async function recordManualDailyPerformance() {
  const response = await fetch("/api/manual-portfolio/record-daily-performance", {
    method: "POST",
  });
  if (!response.ok) {
    window.alert(t("manualSaveFailed"));
    return;
  }
  await refresh();
}

async function deleteManualDailyPerformance(tradeDate) {
  if (!window.confirm(t("deleteDailyPerformanceConfirm"))) {
    return;
  }
  const response = await fetch(
    `/api/manual-portfolio/daily-performance/${encodeURIComponent(tradeDate)}`,
    { method: "DELETE" }
  );
  if (!response.ok) {
    window.alert(t("deleteDailyPerformanceFailed"));
    return;
  }
  await refresh();
}

function renderDerivatives(payload) {
  const summary = payload.summary || {};
  const openPositions = payload.open_positions || [];
  const closedTrades = payload.closed_trades || [];
  const events = payload.events || [];

  els.derivativeOpenCount.textContent = summary.open_count ?? 0;
  els.derivativeOpenPnl.innerHTML = formatSignedVnd(summary.open_pnl_vnd);
  els.derivativeClosedCount.textContent = summary.closed_count ?? 0;
  els.derivativeRealizedPnl.innerHTML = formatSignedVnd(summary.realized_pnl_vnd);
  els.derivativeInitialCapital.textContent = formatVnd(summary.initial_capital);
  els.derivativeCurrentEquity.textContent = formatVnd(summary.current_equity);
  els.derivativeMaxDrawdown.innerHTML = formatDrawdownVnd(summary.max_drawdown_vnd);
  els.derivativeMaxDrawdownPct.innerHTML = formatDrawdownPercent(summary.max_drawdown_pct);
  els.derivativeTotalPnl.innerHTML = formatSignedVnd(summary.total_pnl_vnd);
  els.derivativeTotalReturn.innerHTML = formatSignedPercent(summary.total_return_pct);
  els.derivativeWinningTrades.textContent = summary.closed_count
    ? `${formatPercent(summary.win_rate_pct)} · ${summary.wins}/${summary.closed_count}`
    : "-";
  els.derivativeProfitFactor.textContent = formatRatio(summary.profit_factor);
  if (document.activeElement !== els.derivativeCapitalInput) {
    els.derivativeCapitalInput.value = rawNumber(summary.initial_capital);
  }
  drawDerivativeEquityCurve(payload.equity_curve || []);

  if (!openPositions.length) {
    els.derivativeOpenPositionsTable.innerHTML =
      `<tr><td class="empty" colspan="11">${t("noDerivativePositions")}</td></tr>`;
  } else {
    els.derivativeOpenPositionsTable.innerHTML = openPositions
      .map((position) => `
        <tr>
          <td><strong>${escapeHtml(position.symbol)}</strong></td>
          <td><strong>${escapeHtml(position.strategy)}</strong></td>
          <td><span class="derivativeSide ${escapeHtml(position.side)}">${escapeHtml(position.side)}</span></td>
          <td>${formatPrice(position.average_price)}</td>
          <td>${formatPrice(position.current_price)}</td>
          <td>${formatPrice(position.quantity)}</td>
          <td>${position.layer_count ?? 0}</td>
          <td>${formatSignedNumber(position.pnl_points)}</td>
          <td>${formatSignedVnd(position.pnl_vnd)}</td>
          <td>${formatPrice(position.take_profit)}</td>
          <td>${formatPrice(position.stop_loss)}</td>
        </tr>
      `)
      .join("");
  }

  if (!closedTrades.length) {
    els.derivativeClosedTradesTable.innerHTML =
      `<tr><td class="empty" colspan="11">${t("noDerivativeTrades")}</td></tr>`;
  } else {
    els.derivativeClosedTradesTable.innerHTML = closedTrades
      .map((trade) => `
        <tr>
          <td><strong>${escapeHtml(trade.symbol)}</strong></td>
          <td><strong>${escapeHtml(trade.strategy)}</strong></td>
          <td><span class="derivativeSide ${escapeHtml(trade.side)}">${escapeHtml(trade.side)}</span></td>
          <td>${formatPrice(trade.average_price)}</td>
          <td>${formatPrice(trade.exit_price)}</td>
          <td>${formatPrice(trade.quantity)}</td>
          <td>${trade.layer_count ?? 0}</td>
          <td>${escapeHtml(trade.exit_reason || "-")}</td>
          <td>${formatSignedNumber(trade.pnl_points)}</td>
          <td>${formatSignedVnd(trade.pnl_vnd)}</td>
          <td>${formatDate(trade.exit_time)}</td>
        </tr>
      `)
      .join("");
  }

  if (!events.length) {
    els.derivativeEventsTable.innerHTML =
      `<tr><td class="empty" colspan="8">${t("noDerivativeEvents")}</td></tr>`;
    return;
  }
  els.derivativeEventsTable.innerHTML = events
    .map((event) => `
      <tr>
        <td>${formatDate(event.source_time || event.received_at)}</td>
        <td><strong>${escapeHtml(event.symbol)}</strong></td>
        <td><span class="side ${escapeHtml(event.action)}">${escapeHtml(event.action)}</span></td>
        <td>${formatPrice(event.price)}</td>
        <td>${formatPrice(event.quantity)}</td>
        <td>${escapeHtml(event.strategy || "-")}</td>
        <td>${escapeHtml(event.reason || "-")}</td>
        <td>
          <button class="deleteButton" type="button" data-derivative-delete-id="${event.id}">
            ${escapeHtml(t("delete"))}
          </button>
        </td>
      </tr>
    `)
    .join("");

  els.derivativeEventsTable.querySelectorAll("[data-derivative-delete-id]").forEach((button) => {
    button.addEventListener("click", () => deleteDerivativeEvent(button.dataset.derivativeDeleteId));
  });
}

async function deleteDerivativeEvent(signalId) {
  if (!window.confirm(t("deleteDerivativeConfirm"))) {
    return;
  }
  const response = await fetch(`/api/derivatives/signals/${encodeURIComponent(signalId)}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    window.alert(t("deleteDerivativeFailed"));
    return;
  }
  await refresh();
}

async function saveDerivativeCapital(event) {
  event.preventDefault();
  const initialCapital = parsePriceInput(els.derivativeCapitalInput.value);
  if (!Number.isFinite(initialCapital) || initialCapital <= 0) {
    window.alert(t("derivativeCapitalSaveFailed"));
    return;
  }
  const response = await fetch("/api/settings/derivative-capital", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ initial_capital: initialCapital }),
  });
  if (!response.ok) {
    window.alert(t("derivativeCapitalSaveFailed"));
    return;
  }
  await refresh();
}

function renderDividendEvents() {
  if (!els.dividendEventsTable) return;
  const rows = [...state.dividendEvents].sort((left, right) =>
    String(left.ex_date || "").localeCompare(String(right.ex_date || ""))
  );
  if (!rows.length) {
    els.dividendEventsTable.innerHTML = `<tr><td class="empty" colspan="8">${t("noDividendEvents")}</td></tr>`;
    return;
  }
  els.dividendEventsTable.innerHTML = rows
    .map((event) => `
      <tr class="${event.alert_status === "ex_date_today" ? "exDateRow" : ""}">
        <td><strong>${escapeHtml(event.ticker || "-")}</strong></td>
        <td>${event.alert_status === "ex_date_today"
          ? `<strong>${escapeHtml(t("exDateToday"))}</strong>`
          : `${formatDateOnly(event.ex_date)} (${Number(event.days_until)} ngày)`}</td>
        <td>${formatPrice(event.cash_amount)}</td>
        <td>${formatPercent(event.stock_ratio_pct)}</td>
        <td>${formatPercent(event.issue_ratio_pct)}</td>
        <td>${formatPrice(event.issue_price)}</td>
        <td>${escapeHtml(event.note || "-")}</td>
        <td>
          <button class="deleteButton" type="button" data-dividend-delete-id="${event.id}">${escapeHtml(t("delete"))}</button>
        </td>
      </tr>
    `)
    .join("");

  els.dividendEventsTable.querySelectorAll("[data-dividend-delete-id]").forEach((button) => {
    button.addEventListener("click", () => deleteDividendEvent(button.dataset.dividendDeleteId));
  });
}

function renderExDateAlerts() {
  if (!els.exDateAlerts) return;
  const events = state.dividendEvents.filter((event) => event.alert_status === "ex_date_today");
  if (!events.length) {
    els.exDateAlerts.hidden = true;
    els.exDateAlerts.innerHTML = "";
    return;
  }

  const tickers = [...new Set(events.map((event) => String(event.ticker || "").toUpperCase()))].sort();
  const message = `${t("exDateAlertMessage")}: ${tickers.join(", ")}`;
  els.exDateAlerts.innerHTML = `<strong>${escapeHtml(t("exDateToday"))}</strong>: ${escapeHtml(tickers.join(", "))}`;
  els.exDateAlerts.hidden = false;

  const alertKey = `dividendExDateAlert:${localMarketDate()}:${tickers.join(",")}`;
  if (localStorage.getItem(alertKey) !== "shown") {
    localStorage.setItem(alertKey, "shown");
    window.alert(message);
  }
}

function localMarketDate() {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Ho_Chi_Minh",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date());
}

async function addDividendEvent(event) {
  event.preventDefault();
  const body = {
    ticker: els.dividendTicker.value.trim().toUpperCase(),
    ex_date: els.dividendExDate.value,
    cash_amount: optionalNumber(els.dividendCashAmount.value),
    stock_ratio_pct: optionalNumber(els.dividendStockRatio.value),
    issue_ratio_pct: optionalNumber(els.dividendIssueRatio.value),
    issue_price: optionalNumber(els.dividendIssuePrice.value),
    note: els.dividendNote.value.trim() || null,
  };
  const response = await fetch("/api/dividend-events", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    window.alert(t("dividendSaveFailed"));
    return;
  }
  els.dividendEventForm.reset();
  await refresh();
}

async function deleteDividendEvent(eventId) {
  if (!window.confirm(t("dividendDeleteConfirm"))) {
    return;
  }
  const response = await fetch(`/api/dividend-events/${encodeURIComponent(eventId)}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    window.alert(t("dividendDeleteFailed"));
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
  const confirmFilter = els.openPositionConfirmFilter.value;
  return openTrades.filter((trade) => {
    const tickerMatches = !tickerFilter || String(trade.ticker || "").includes(tickerFilter);
    const strategyMatches =
      !strategyFilter || String(trade.strategy || "").toLowerCase().includes(strategyFilter);
    const confirmMatches =
      confirmFilter === "all" ||
      (confirmFilter === "confirmed" && trade.has_confirm_buy) ||
      (confirmFilter === "unconfirmed" && !trade.has_confirm_buy);
    return tickerMatches && strategyMatches && confirmMatches;
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
    els.performanceTable.innerHTML = `<tr><td class="empty" colspan="9">${t("noTrades")}</td></tr>`;
    return;
  }

  els.performanceTable.innerHTML = strategies
    .map((strategy) => `
      <tr class="clickableRow" data-performance-ticker="${escapeHtml(strategy.ticker)}" data-performance-strategy="${escapeHtml(strategy.strategy)}">
        <td><strong>${escapeHtml(strategy.ticker)}</strong></td>
        <td><strong>${escapeHtml(strategy.strategy)}</strong></td>
        <td>${formatPercent(state.defaultSignalWeightPct)}</td>
        <td>${strategy.closed_trades}</td>
        <td>${strategy.open_trades}</td>
        <td>${formatPercent(strategy.win_rate_pct)}</td>
        <td>${formatSignedPercent(strategy.closed_trades ? allocatedReturnPct(strategy.realized_return_pct) : null)}</td>
        <td>${formatSignedPercent(strategy.open_trades ? allocatedReturnPct(strategy.open_return_avg_pct) : null)}</td>
        <td>${formatSignedPercent(allocatedReturnPct(strategy.current_return_pct))}</td>
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
  renderOpenPositionsTotalReturn(openTrades);
  if (!openTrades.length) {
    els.openPositionsTable.innerHTML = `<tr><td class="empty" colspan="9">${t("noOpenPositions")}</td></tr>`;
    return;
  }

  els.openPositionsTable.innerHTML = openTrades
    .map((trade) => {
      const tickerClass = trade.has_confirm_buy ? "confirmedTicker" : "";
      const confirmTitle = trade.has_confirm_buy ? t("confirmBuyTitle") : "";
      return `
      <tr data-ticker="${escapeHtml(trade.ticker)}">
        <td><strong class="${tickerClass}" title="${escapeHtml(confirmTitle)}">${escapeHtml(trade.ticker)}</strong></td>
        <td><strong>${escapeHtml(trade.strategy)}</strong></td>
        <td>${formatPrice(trade.entry_price)}</td>
        <td>${formatPrice(trade.exit_price)}</td>
        <td>${formatSignedPercent(trade.return_pct)}</td>
        <td>${renderConfirmations(trade.confirmations || [])}</td>
        <td>${renderDividendNotes(trade.dividend_notes || [])}</td>
        <td>${formatHoldingDaysBetween(trade.entry_time)}</td>
        <td>${formatDate(trade.entry_time)}</td>
      </tr>
    `;
    })
    .join("");

  els.openPositionsTable.querySelectorAll("[data-ticker]").forEach((row) => {
    row.addEventListener("click", () => renderChart(row.dataset.ticker));
  });
}

function renderConfirmations(confirmations) {
  if (!confirmations.length) {
    return `<span class="mutedText">${escapeHtml(t("noConfirmations"))}</span>`;
  }
  return `
    <div class="confirmTimeline">
      ${confirmations
        .map((confirmation) => `
          <span class="confirmBadge" title="${escapeHtml(formatDate(confirmation.time))}">
            ${escapeHtml(confirmation.strategy || confirmation.action || "-")}
            <small>${escapeHtml(formatPrice(confirmation.price))} · ${escapeHtml(formatDateOnly(confirmation.time))}</small>
          </span>
        `)
        .join("")}
    </div>
  `;
}

function renderDividendNotes(notes) {
  if (!notes.length) {
    return `<span class="mutedText">${escapeHtml(t("noDividends"))}</span>`;
  }
  return `
    <div class="confirmTimeline">
      ${notes
        .map((note) => {
          const isApplied = note.status === "applied";
          const label = isApplied ? t("appliedDividend") : t("upcomingDividend");
          const detail = [
            note.cash_amount ? `${formatPrice(note.cash_amount)} cash` : "",
            note.stock_ratio_pct ? `${formatPercent(note.stock_ratio_pct)} stock` : "",
            note.issue_ratio_pct ? `${formatPercent(note.issue_ratio_pct)} issue` : "",
            note.issue_price ? `${formatPrice(note.issue_price)} price` : "",
            note.days_until !== undefined ? `${note.days_until}d` : "",
          ].filter(Boolean).join(" · ");
          return `
            <span class="dividendBadge ${isApplied ? "applied" : "upcoming"}" title="${escapeHtml(note.note || "")}">
              ${escapeHtml(label)}
              <small>${escapeHtml(formatDateOnly(note.ex_date))}${detail ? ` · ${escapeHtml(detail)}` : ""}</small>
            </span>
          `;
        })
        .join("")}
    </div>
  `;
}

function renderOpenPositionsTotalReturn(openTrades) {
  const totalReturn = openTrades.reduce((sum, trade) => {
    const value = allocatedReturnPct(trade.return_pct);
    return Number.isFinite(value) ? sum + value : sum;
  }, 0);
  els.openPositionsTotalReturn.innerHTML = openTrades.length
    ? formatSignedPercent(totalReturn)
    : "-";
}

function renderClosedTrades(closedTrades) {
  const filtered = filterClosedTrades(closedTrades);
  updateClosedTradesFilterLabel();
  const sorted = [...filtered].sort((left, right) =>
    String(right.exit_time || "").localeCompare(String(left.exit_time || ""))
  );

  if (!sorted.length) {
    els.closedTradesTable.innerHTML = `<tr><td class="empty" colspan="10">${t("noClosedTrades")}</td></tr>`;
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
        <td>${formatPercent(state.defaultSignalWeightPct)}</td>
        <td>${formatSignedPercent(allocatedReturnPct(trade.return_pct))}</td>
        <td>${formatDuration(trade.holding_seconds)}</td>
        <td>${formatDate(trade.exit_time)}</td>
        <td>
          ${trade.exit_signal_id ? `
            <button class="restoreButton" type="button" data-reopen-exit-id="${escapeHtml(trade.exit_signal_id)}" title="${escapeHtml(t("reopenPositionTitle"))}">
              ${escapeHtml(t("reopenPosition"))}
            </button>
          ` : "-"}
        </td>
      </tr>
    `)
    .join("");

  els.closedTradesTable.querySelectorAll("[data-ticker]").forEach((row) => {
    row.addEventListener("click", () => renderChart(row.dataset.ticker));
  });
  els.closedTradesTable.querySelectorAll("[data-reopen-exit-id]").forEach((button) => {
    button.addEventListener("click", async (event) => {
      event.stopPropagation();
      await reopenClosedTrade(button.dataset.reopenExitId);
    });
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
    base_strategy_not_open: "baseStrategyNotOpen",
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
    const allocatedReturn = allocatedReturnPct(trade.return_pct) || 0;
    points.push({
      value: previous * (1 + allocatedReturn / 100),
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

function drawDerivativeEquityCurve(curve) {
  const canvas = els.derivativeEquityCanvas;
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.max(1, Math.floor(rect.width * dpr));
  canvas.height = Math.max(1, Math.floor(rect.height * dpr));
  ctx.scale(dpr, dpr);
  ctx.clearRect(0, 0, rect.width, rect.height);

  const points = (curve || [])
    .map((point) => ({
      equity: Number(point.equity),
      drawdown: Number(point.drawdown_vnd || 0),
    }))
    .filter((point) => Number.isFinite(point.equity));
  if (points.length < 2) {
    ctx.fillStyle = cssVar("--muted") || "#66727a";
    ctx.font = "14px system-ui";
    ctx.fillText(t("noDerivativeTrades"), 18, 38);
    return;
  }

  const pad = { top: 24, right: 76, bottom: 32, left: 18 };
  const width = rect.width - pad.left - pad.right;
  const height = rect.height - pad.top - pad.bottom;
  const values = points.map((point) => point.equity);
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;
  const maxDrawdown = Math.max(...points.map((point) => point.drawdown), 1);

  ctx.strokeStyle = cssVar("--line") || "#dbe2df";
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i += 1) {
    const y = pad.top + (height / 4) * i;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(rect.width - pad.right, y);
    ctx.stroke();
    ctx.fillStyle = cssVar("--muted") || "#66727a";
    ctx.font = "12px system-ui";
    ctx.fillText(compactVnd(max - (range / 4) * i), rect.width - pad.right + 8, y + 4);
  }

  const stepX = width / Math.max(1, points.length - 1);
  const barWidth = Math.max(2, Math.min(12, stepX * 0.55));
  points.forEach((point, index) => {
    if (point.drawdown <= 0) return;
    const x = pad.left + stepX * index;
    const barHeight = (point.drawdown / maxDrawdown) * (height * 0.34);
    ctx.fillStyle = "rgba(202, 62, 62, 0.45)";
    ctx.fillRect(x - barWidth / 2, pad.top + height - barHeight, barWidth, barHeight);
  });

  ctx.strokeStyle = cssVar("--buy") || "#16a085";
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  points.forEach((point, index) => {
    const x = pad.left + stepX * index;
    const y = pad.top + height - ((point.equity - min) / range) * height;
    if (index === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();

  const last = points[points.length - 1];
  ctx.fillStyle = cssVar("--ink") || "#152025";
  ctx.font = "700 12px system-ui";
  ctx.fillText(formatVnd(last.equity), pad.left, rect.height - 9);
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

async function reopenClosedTrade(exitSignalId) {
  if (!window.confirm(t("reopenPositionConfirm"))) {
    return;
  }
  const response = await fetch(`/api/signals/${encodeURIComponent(exitSignalId)}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    window.alert(t("reopenPositionFailed"));
    return;
  }
  await refresh();
}

async function renderChart(ticker) {
  const requestId = ++priceChartState.requestId;
  state.selectedTicker = ticker;
  els.chartTitle.textContent = ticker;
  renderTickerTimeline(ticker);
  let payload;
  try {
    payload = await fetchJson(`/api/chart/${encodeURIComponent(ticker)}`);
  } catch (error) {
    if (requestId === priceChartState.requestId) {
      console.error(`Failed to load chart for ${ticker}`, error);
      clearChart(t("noHistory"));
    }
    return;
  }
  if (requestId !== priceChartState.requestId) return;
  drawCandles(
    normalizeHistory(payload.history || []),
    normalizeMarkers(payload.markers || []),
    ticker
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
  const rowsByTime = new Map();
  history
    .map((row) => ({
      time: normalizeChartTime(row.time || row.date || row.tradingDate || row.trading_date || ""),
      open: Number(row.open ?? row.Open ?? row.openPrice ?? row.o),
      high: Number(row.high ?? row.High ?? row.highPrice ?? row.h),
      low: Number(row.low ?? row.Low ?? row.lowPrice ?? row.l),
      close: Number(row.close ?? row.Close ?? row.closePrice ?? row.c),
      volume: Number(row.volume ?? row.Volume ?? row.v ?? 0),
    }))
    .filter((row) =>
      row.time && [row.open, row.high, row.low, row.close].every((value) => Number.isFinite(value))
    )
    .forEach((row) => rowsByTime.set(row.time, row));
  return [...rowsByTime.values()].sort((left, right) => left.time.localeCompare(right.time));
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

function drawCandles(rows, markers = [], ticker = "") {
  ensurePriceChart();
  if (!rows.length) {
    clearChart(t("noHistory"));
    return;
  }

  els.chartEmpty.hidden = true;
  priceChartState.candleSeries.setData(rows.map(({ time, open, high, low, close }) => ({
    time,
    open,
    high,
    low,
    close,
  })));
  priceChartState.volumeSeries.setData(rows
    .filter((row) => Number.isFinite(row.volume) && row.volume > 0)
    .map((row) => ({
      time: row.time,
      value: row.volume,
      color: row.close >= row.open
        ? colorWithAlpha(cssVar("--buy") || "#078465", 0.42)
        : colorWithAlpha(cssVar("--sell") || "#c2413a", 0.42),
    })));
  priceChartState.markerPlugin.setMarkers(toSeriesMarkers(markers, rows));

  if (priceChartState.ticker !== ticker) {
    priceChartState.chart.timeScale().fitContent();
  }
  priceChartState.ticker = ticker;
}

function ensurePriceChart() {
  if (priceChartState.chart) return;
  if (!window.LightweightCharts) {
    throw new Error("Lightweight Charts failed to load");
  }

  const chart = window.LightweightCharts.createChart(els.chart, {
    width: Math.max(1, els.chart.clientWidth),
    height: Math.max(1, els.chart.clientHeight),
    localization: { locale: state.language === "vi" ? "vi-VN" : "en-US" },
    rightPriceScale: { borderVisible: false },
    timeScale: {
      borderVisible: false,
      timeVisible: false,
      secondsVisible: false,
      rightOffset: 5,
    },
    crosshair: { mode: window.LightweightCharts.CrosshairMode.MagnetOHLC },
  });
  const candleSeries = chart.addSeries(window.LightweightCharts.CandlestickSeries, {
    upColor: cssVar("--buy") || "#078465",
    downColor: cssVar("--sell") || "#c2413a",
    borderVisible: false,
    wickUpColor: cssVar("--buy") || "#078465",
    wickDownColor: cssVar("--sell") || "#c2413a",
    priceFormat: { type: "price", precision: 2, minMove: 0.01 },
  });
  const volumeSeries = chart.addSeries(window.LightweightCharts.HistogramSeries, {
    priceFormat: { type: "volume" },
    priceScaleId: "volume",
    lastValueVisible: false,
    priceLineVisible: false,
  });
  chart.priceScale("volume").applyOptions({
    scaleMargins: { top: 0.82, bottom: 0 },
  });

  priceChartState.chart = chart;
  priceChartState.candleSeries = candleSeries;
  priceChartState.volumeSeries = volumeSeries;
  priceChartState.markerPlugin = window.LightweightCharts.createSeriesMarkers(candleSeries, []);
  priceChartState.resizeObserver = new ResizeObserver(resizePriceChart);
  priceChartState.resizeObserver.observe(els.chart);
  applyPriceChartTheme();
}

function applyPriceChartTheme() {
  if (!priceChartState.chart) return;
  const buy = cssVar("--buy") || "#078465";
  const sell = cssVar("--sell") || "#c2413a";
  priceChartState.chart.applyOptions({
    layout: {
      background: { type: window.LightweightCharts.ColorType.Solid, color: cssVar("--panel") || "#ffffff" },
      textColor: cssVar("--muted") || "#64748b",
      attributionLogo: false,
    },
    grid: {
      vertLines: { color: cssVar("--line-soft") || "#edf1f6" },
      horzLines: { color: cssVar("--line-soft") || "#edf1f6" },
    },
    localization: { locale: state.language === "vi" ? "vi-VN" : "en-US" },
  });
  priceChartState.candleSeries.applyOptions({
    upColor: buy,
    downColor: sell,
    wickUpColor: buy,
    wickDownColor: sell,
  });
}

function resizePriceChart() {
  if (!priceChartState.chart) return;
  priceChartState.chart.resize(
    Math.max(1, els.chart.clientWidth),
    Math.max(1, els.chart.clientHeight)
  );
}

function toSeriesMarkers(markers, rows) {
  if (!markers.length || !rows.length) return [];
  const availableTimes = rows.map((row) => row.time);
  const availableSet = new Set(availableTimes);
  return markers
    .map((marker) => {
      const requestedTime = normalizeChartTime(marker.time);
      const time = availableSet.has(requestedTime)
        ? requestedTime
        : nearestChartTime(availableTimes, requestedTime);
      if (!time) return null;
      const isBuy = marker.action === "buy";
      return {
        time,
        position: isBuy ? "belowBar" : "aboveBar",
        color: isBuy ? cssVar("--buy") || "#078465" : cssVar("--sell") || "#c2413a",
        shape: isBuy ? "arrowUp" : "arrowDown",
        text: isBuy ? "B" : "S",
      };
    })
    .filter(Boolean)
    .sort((left, right) => left.time.localeCompare(right.time));
}

function nearestChartTime(availableTimes, requestedTime) {
  const target = Date.parse(requestedTime);
  if (!Number.isFinite(target)) return "";
  let nearest = "";
  let distance = Number.POSITIVE_INFINITY;
  availableTimes.forEach((time) => {
    const candidate = Date.parse(time);
    const candidateDistance = Math.abs(candidate - target);
    if (Number.isFinite(candidateDistance) && candidateDistance < distance) {
      nearest = time;
      distance = candidateDistance;
    }
  });
  return nearest;
}

function normalizeChartTime(value) {
  if (!value) return "";
  const text = String(value);
  const datePrefix = text.match(/^(\d{4}-\d{2}-\d{2})/);
  if (datePrefix) return datePrefix[1];
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Ho_Chi_Minh",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(date);
}

function colorWithAlpha(color, alpha) {
  const hex = String(color || "").replace("#", "");
  if (!/^[0-9a-f]{6}$/i.test(hex)) return color;
  const red = Number.parseInt(hex.slice(0, 2), 16);
  const green = Number.parseInt(hex.slice(2, 4), 16);
  const blue = Number.parseInt(hex.slice(4, 6), 16);
  return `rgba(${red}, ${green}, ${blue}, ${alpha})`;
}

function clearChart(message) {
  ensurePriceChart();
  priceChartState.candleSeries.setData([]);
  priceChartState.volumeSeries.setData([]);
  priceChartState.markerPlugin.setMarkers([]);
  priceChartState.ticker = "";
  els.chartEmpty.textContent = message;
  els.chartEmpty.hidden = false;
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

function formatSignedNumber(value) {
  if (value === null || value === undefined) return "-";
  const number = Number(value);
  const className = number >= 0 ? "positive" : "negative";
  const sign = number > 0 ? "+" : "";
  return `<span class="${className}">${sign}${number.toLocaleString(undefined, { maximumFractionDigits: 2 })}</span>`;
}

function formatSignedVnd(value) {
  if (value === null || value === undefined) return "-";
  const number = Number(value);
  const className = number >= 0 ? "positive" : "negative";
  const sign = number > 0 ? "+" : "";
  return `<span class="${className}">${sign}${number.toLocaleString("vi-VN", { maximumFractionDigits: 0 })} đ</span>`;
}

function formatVnd(value) {
  if (value === null || value === undefined) return "-";
  return `${Number(value).toLocaleString("vi-VN", { maximumFractionDigits: 0 })} đ`;
}

function compactVnd(value) {
  return Number(value).toLocaleString("vi-VN", {
    notation: "compact",
    maximumFractionDigits: 1,
  });
}

function formatRatio(value) {
  if (value === null || value === undefined || !Number.isFinite(Number(value))) return "-";
  return Number(value).toFixed(3);
}

function formatDrawdownVnd(value) {
  if (value === null || value === undefined) return "-";
  const number = Number(value);
  if (number === 0) return "0 đ";
  return `<span class="negative">-${number.toLocaleString("vi-VN", { maximumFractionDigits: 0 })} đ</span>`;
}

function formatDrawdownPercent(value) {
  if (value === null || value === undefined) return "-";
  const number = Number(value);
  if (number === 0) return "0.00%";
  return `<span class="negative">-${number.toFixed(2)}%</span>`;
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
els.loginForm.addEventListener("submit", submitLogin);
els.logoutButton.addEventListener("click", logout);
els.userCreateForm.addEventListener("submit", createAdminUser);
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
els.openPositionConfirmFilter.addEventListener("change", renderOpenPositions);
els.openPositionSort.addEventListener("change", renderOpenPositions);
els.openPositionRefreshPrices.addEventListener("click", refreshOpenPositionMarketPrices);
els.performanceTickerFilter.addEventListener("input", refresh);
els.performanceStrategyFilter.addEventListener("input", refresh);
els.performanceSort.addEventListener("change", refresh);
els.clearClosedTradesFilter.addEventListener("click", clearClosedTradeFilter);
els.manualPositionForm.addEventListener("submit", addManualPosition);
els.manualRefreshPrices.addEventListener("click", refreshManualMarketPrices);
els.manualRecordDailyPerformance.addEventListener("click", recordManualDailyPerformance);
els.dividendEventForm.addEventListener("submit", addDividendEvent);
els.derivativeCapitalForm.addEventListener("submit", saveDerivativeCapital);
window.addEventListener("resize", () => {
  resizePriceChart();
  if (state.activeTab === "manualPortfolio") {
    drawManualEquityCurve(state.manualPortfolio.equity_curve || []);
  }
  if (state.activeTab === "derivatives") {
    drawDerivativeEquityCurve(state.derivatives.equity_curve || []);
  }
});

applyTheme();
applyTranslations();
updateWatchlistControls();
bootstrapAuth();
setInterval(refresh, 15000);
