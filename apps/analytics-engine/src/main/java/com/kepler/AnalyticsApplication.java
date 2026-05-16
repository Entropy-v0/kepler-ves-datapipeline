package com.kepler;

import com.kepler.analytics.MarketAnalyzer;
import com.kepler.db.DatabaseConnection;
import com.kepler.model.MarketReport;
import com.kepler.report.ReportExporter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Entry point for the Kepler Analytics Engine.
 * Runs a timed loop that reads from PostgreSQL, computes market metrics,
 * and exports structured reports every ANALYTICS_INTERVAL_SECONDS seconds.
 */
public class AnalyticsApplication {

    private static final Logger log = LoggerFactory.getLogger(AnalyticsApplication.class);
    private static volatile boolean running = true;

    public static void main(String[] args) throws InterruptedException {
        log.info("--- Kepler Analytics Engine ONLINE ---");

        // Graceful shutdown on SIGTERM / SIGINT
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            log.info("Shutdown signal received. Stopping analytics loop...");
            running = false;
        }));

        String intervalEnv = System.getenv("ANALYTICS_INTERVAL_SECONDS");
        int intervalSeconds = 300;
        if (intervalEnv != null && !intervalEnv.trim().isEmpty()) {
            try {
                intervalSeconds = Integer.parseInt(intervalEnv.trim());
            } catch (NumberFormatException e) {
                log.warn("Invalid ANALYTICS_INTERVAL_SECONDS value: '{}', defaulting to 300", intervalEnv);
            }
        }

        DatabaseConnection db = new DatabaseConnection();
        MarketAnalyzer analyzer = new MarketAnalyzer(db);
        ReportExporter exporter = new ReportExporter();

        while (running) {
            try {
                log.info("Starting analytics cycle...");
                MarketReport report = analyzer.analyze();

                if (report != null) {
                    exporter.export(report);
                } else {
                    log.warn("No recent data available. Is Kepler running?");
                }

            } catch (Exception e) {
                log.error("Error during analytics cycle: {}", e.getMessage(), e);
            }

            log.debug("Next cycle in {} seconds...", intervalSeconds);
            Thread.sleep(intervalSeconds * 1000L);
        }

        log.info("Analytics engine stopped gracefully.");
    }
}
