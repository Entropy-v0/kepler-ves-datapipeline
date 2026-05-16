package com.kepler.analytics;

import com.kepler.db.DatabaseConnection;
import com.kepler.model.MarketMetrics;
import com.kepler.model.MarketReport;
import com.kepler.repository.P2PAdsRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.SQLException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Map;

/**
 * Core analytics engine.
 * Reads aggregated metrics from PostgreSQL, saves them, and produces a MarketReport.
 */
public class MarketAnalyzer {

    private static final Logger log = LoggerFactory.getLogger(MarketAnalyzer.class);
    private static final DateTimeFormatter FMT = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    private final P2PAdsRepository repository;

    public MarketAnalyzer(DatabaseConnection db) {
        this.repository = new P2PAdsRepository(db);
    }

    /**
     * Runs one full analysis cycle.
     *
     * @return a populated {@link MarketReport}, or null if there is no recent data.
     */
    public MarketReport analyze() throws SQLException {

        if (!repository.hasRecentData()) {
            return null;
        }

        // Fetch aggregated metrics directly from DB
        List<MarketMetrics> metricsList = repository.getAggregatedMetrics();

        MarketMetrics buyMetrics = metricsList.stream()
            .filter(m -> "BUY".equals(m.getTradeType()))
            .findFirst()
            .orElse(null);

        MarketMetrics sellMetrics = metricsList.stream()
            .filter(m -> "SELL".equals(m.getTradeType()))
            .findFirst()
            .orElse(null);

        if (buyMetrics == null || sellMetrics == null) {
            log.warn("Incomplete data for analysis. Found metrics: {}", metricsList.size());
            return null;
        }

        // Assign timestamp and save to DB
        String timestamp = LocalDateTime.now().format(FMT);
        buyMetrics.setTimestamp(timestamp);
        sellMetrics.setTimestamp(timestamp);

        repository.saveMetrics(buyMetrics);
        repository.saveMetrics(sellMetrics);

        // ── Calculate Spread ───────────────────────────────────────────────────
        double avgBuy = buyMetrics.getAvgPrice();
        double avgSell = sellMetrics.getAvgPrice();
        double spread = avgBuy - avgSell;
        double spreadPct = avgSell > 0 ? (spread / avgSell) * 100.0 : 0.0;

        // ── Fetch DB-side queries for top merchants and bank ──────────────────
        Map<String, String> topMerchants = repository.getTopMerchantPerSide();
        String dominantBank = repository.getDominantBank();

        // ── Assemble report ───────────────────────────────────────────────────
        MarketReport report = new MarketReport();
        report.setTimestamp(timestamp);
        report.setAvgPriceBuy(avgBuy);
        report.setAvgPriceSell(avgSell);
        report.setSpread(spread);
        report.setSpreadPct(spreadPct);
        report.setPriceRangeBuy(buyMetrics.getPriceRange());
        report.setPriceRangeSell(sellMetrics.getPriceRange());
        report.setTopMerchantBuy(topMerchants.getOrDefault("BUY", "N/A"));
        report.setTopMerchantSell(topMerchants.getOrDefault("SELL", "N/A"));
        report.setDominantBank(dominantBank);
        report.setTotalRecordsBuy(buyMetrics.getRecordCount());
        report.setTotalRecordsSell(sellMetrics.getRecordCount());

        log.info("Analysis complete | BUY: {} VES | SELL: {} VES | Spread: {} VES ({}%)",
            String.format("%.2f", avgBuy),
            String.format("%.2f", avgSell),
            String.format("%.2f", spread),
            String.format("%.3f", spreadPct));

        return report;
    }
}
