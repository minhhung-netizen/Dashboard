// Static configuration data (defaults, presets, labels) shared with app.js.
// Loaded as a plain script before app.js; these are read-only globals.

const FALLBACK_SIGNAL_WEIGHT_PCT = 5;
const NUMBER_FORMAT_LOCALE = "en-US";
const KELLY_STORAGE_KEY = "dashboardKellyInputs";
const KELLY_LIST_STORAGE_KEY = "dashboardKellyEntries";
const DCA_RISK_LIMIT_STORAGE_KEY = "dashboardDcaRiskLimitPct";
const DEFAULT_DCA_RISK_LIMIT_PCT = 1.5;
const DEFAULT_KELLY_INPUTS = {
  ticker: "",
  strategy: "",
  winRate: 50.64,
  winningTrades: 79,
  totalTrades: 156,
  profitFactor: 2.269,
  maxDrawdown: 3.63,
  targetDrawdown: 10,
  fraction: 50,
  maxAllocation: 20,
};
const DEFAULT_DCA_LEVELS = [
  { distancePct: 0, multiplier: 1 },
  { distancePct: 5, multiplier: 1 },
  { distancePct: 10, multiplier: 1.5 },
  { distancePct: 15, multiplier: 2 },
  { distancePct: 20, multiplier: 2.5 },
];
const DCA_PRESETS = {
  conservative: {
    multipliers: [1, 1, 1.2, 1.5, 1.8],
  },
  balanced: {
    multipliers: [1, 1, 1.5, 2, 2.5],
  },
  aggressive: {
    multipliers: [1, 1.5, 2, 2.5, 3],
  },
};
const STRATEGY_DISPLAY_ALIASES = {
  stxanhdo: "ST",
  "mordern stock ema": "MSE",
  "modern stock ema": "MSE",
};
const FEATURE_LABELS = {
  overview: "Tổng quan",
  positions: "Vị thế",
  derivatives: "Phái sinh VN30",
  manualPortfolio: "Danh mục tay",
  performance: "Hiệu suất",
  kelly: "Kelly",
  dcaSizing: "Phân bổ DCA",
  dividends: "Cổ tức",
  logs: "Nhật ký",
};
