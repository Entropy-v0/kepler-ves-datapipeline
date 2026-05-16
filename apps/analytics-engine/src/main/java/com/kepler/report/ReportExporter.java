package com.kepler.report;

import com.kepler.model.MarketReport;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.*;
import java.time.LocalDate;

/**
 * Exports a {@link MarketReport} to two destinations:
 * <ol>
 *   <li>Structured log output (visible in docker compose logs)</li>
 *   <li>Daily rolling CSV file at /app/data/analytics/YYYY-MM-DD_market_report.csv</li>
 * </ol>
 */
public class ReportExporter {

    private static final Logger log = LoggerFactory.getLogger(ReportExporter.class);
    private static final String BASE_DIR = "/app/data/analytics";

    private static final String CSV_HEADER =
        "timestamp,avg_price_buy,avg_price_sell,spread_ves,spread_pct," +
        "price_range_buy,price_range_sell,top_merchant_buy,top_merchant_sell," +
        "dominant_bank,total_records_buy,total_records_sell";

    public void export(MarketReport report) {
        logReport(report);
        writeCsv(report);
    }

    // ── Structured log output ────────────────────────────────────────────────

    private void logReport(MarketReport report) {
        log.info("╔══════════════ MARKET REPORT [VES/USDT] ══════════════╗");
        log.info("  Timestamp      : {}", report.getTimestamp());
        log.info("  BUY  avg price : {} VES", String.format("%.2f", report.getAvgPriceBuy()));
        log.info("  SELL avg price : {} VES", String.format("%.2f", report.getAvgPriceSell()));
        log.info("  Spread         : {} VES  ({}%)",
            String.format("%.2f", report.getSpread()),
            String.format("%.3f", report.getSpreadPct()));
        log.info("  Range BUY      : {} VES", String.format("%.2f", report.getPriceRangeBuy()));
        log.info("  Range SELL     : {} VES", String.format("%.2f", report.getPriceRangeSell()));
        log.info("  Top BUY merch  : {}", report.getTopMerchantBuy());
        log.info("  Top SELL merch : {}", report.getTopMerchantSell());
        log.info("  Dominant bank  : {}", report.getDominantBank());
        log.info("  Records        : {} BUY / {} SELL",
            report.getTotalRecordsBuy(), report.getTotalRecordsSell());
        log.info("╚══════════════════════════════════════════════════════╝");
    }

    // ── Daily rolling CSV ────────────────────────────────────────────────────

    private void writeCsv(MarketReport report) {
        String date     = LocalDate.now().toString();
        String fileName = date + "_market_report.csv";
        Path   filePath = Paths.get(BASE_DIR, fileName);

        try {
            Files.createDirectories(Paths.get(BASE_DIR));
            boolean isNewFile = !Files.exists(filePath);

            try (BufferedWriter writer = Files.newBufferedWriter(filePath,
                     StandardOpenOption.CREATE, StandardOpenOption.APPEND)) {

                if (isNewFile) {
                    writer.write(CSV_HEADER);
                    writer.newLine();
                }
                writer.write(report.toCsvRow());
                writer.newLine();
            }
            log.debug("Report appended to: {}", filePath);

        } catch (IOException e) {
            log.error("Failed to write CSV report: {}", e.getMessage());
        }
    }
}
