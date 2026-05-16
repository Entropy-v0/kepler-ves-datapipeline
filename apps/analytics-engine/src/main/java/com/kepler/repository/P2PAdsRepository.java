package com.kepler.repository;

import com.kepler.db.DatabaseConnection;
import com.kepler.model.MarketMetrics;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.*;
import java.util.*;

/**
 * Encapsulates all SQL queries against the p2p_ads table.
 * Each method opens, uses, and closes its own connection (safe for long-running apps).
 */
public class P2PAdsRepository {

    private static final Logger log = LoggerFactory.getLogger(P2PAdsRepository.class);

    // Window of data to consider "recent" for each analysis cycle
    private static final String WINDOW = "10 minutes";

    private final DatabaseConnection db;

    public P2PAdsRepository(DatabaseConnection db) {
        this.db = db;
    }

    /**
     * Returns true if there are records in the analysis window.
     * Used as a guard before running expensive queries.
     */
    public boolean hasRecentData() throws SQLException {
        String sql = "SELECT COUNT(*) FROM p2p_ads " +
                     "WHERE timestamp::timestamp >= NOW() - INTERVAL '" + WINDOW + "'";

        try (Connection conn = db.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            return rs.next() && rs.getInt(1) > 0;
        }
    }

    /**
     * Obtains aggregated market metrics for both BUY and SELL sides directly from PostgreSQL.
     * Uses STDDEV and PERCENTILE_CONT for statistical accuracy.
     */
    public List<MarketMetrics> getAggregatedMetrics() throws SQLException {
        String sql = "SELECT trade_type, " +
                     "       AVG(price) AS avg_price, " +
                     "       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) AS median_price, " +
                     "       COALESCE(STDDEV(price), 0) AS std_dev, " +
                     "       MAX(price) - MIN(price) AS price_range, " +
                     "       COUNT(*) AS record_count " +
                     "FROM p2p_ads " +
                     "WHERE timestamp::timestamp >= NOW() - INTERVAL '" + WINDOW + "' " +
                     "GROUP BY trade_type";

        List<MarketMetrics> metricsList = new ArrayList<>();
        try (Connection conn = db.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                MarketMetrics m = new MarketMetrics();
                m.setTradeType(rs.getString("trade_type"));
                m.setAvgPrice(rs.getDouble("avg_price"));
                m.setMedianPrice(rs.getDouble("median_price"));
                m.setStdDev(rs.getDouble("std_dev"));
                m.setPriceRange(rs.getDouble("price_range"));
                m.setRecordCount(rs.getInt("record_count"));
                metricsList.add(m);
            }
        }
        log.debug("Loaded aggregated metrics from last {}", WINDOW);
        return metricsList;
    }

    /**
     * Saves the computed metrics into the market_metrics table.
     * Ensures the table exists before attempting to insert.
     */
    public void saveMetrics(MarketMetrics metrics) throws SQLException {
        String createTableSql = "CREATE TABLE IF NOT EXISTS market_metrics (" +
                                "id SERIAL PRIMARY KEY, " +
                                "timestamp TIMESTAMP, " +
                                "trade_type VARCHAR(10), " +
                                "avg_price NUMERIC, " +
                                "median_price NUMERIC, " +
                                "std_dev NUMERIC, " +
                                "price_range NUMERIC, " +
                                "record_count INT)";

        String insertSql = "INSERT INTO market_metrics (timestamp, trade_type, avg_price, median_price, std_dev, price_range, record_count) " +
                           "VALUES (?::timestamp, ?, ?, ?, ?, ?, ?)";

        try (Connection conn = db.getConnection()) {
            try (Statement stmt = conn.createStatement()) {
                stmt.execute(createTableSql);
            }
            try (PreparedStatement stmt = conn.prepareStatement(insertSql)) {
                stmt.setString(1, metrics.getTimestamp());
                stmt.setString(2, metrics.getTradeType());
                stmt.setDouble(3, metrics.getAvgPrice());
                stmt.setDouble(4, metrics.getMedianPrice());
                stmt.setDouble(5, metrics.getStdDev());
                stmt.setDouble(6, metrics.getPriceRange());
                stmt.setInt(7, metrics.getRecordCount());
                stmt.executeUpdate();
            }
        }
        log.debug("Saved metrics for side: {}", metrics.getTradeType());
    }

    /**
     * Returns the merchant with the highest total available amount per trade side.
     * Key: "BUY" or "SELL", Value: merchant nickname.
     */
    public Map<String, String> getTopMerchantPerSide() throws SQLException {
        String sql =
            "SELECT trade_type, merchant FROM (" +
            "  SELECT trade_type, merchant, SUM(available) AS total_available, " +
            "         ROW_NUMBER() OVER (PARTITION BY trade_type ORDER BY SUM(available) DESC) AS rn " +
            "  FROM p2p_ads " +
            "  WHERE timestamp::timestamp >= NOW() - INTERVAL '" + WINDOW + "' " +
            "  GROUP BY trade_type, merchant" +
            ") sub WHERE rn = 1";

        Map<String, String> result = new HashMap<>();
        try (Connection conn = db.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            while (rs.next()) {
                result.put(rs.getString("trade_type"), rs.getString("merchant"));
            }
        }
        return result;
    }

    /**
     * Returns the most frequently listed payment method in the analysis window.
     */
    public String getDominantBank() throws SQLException {
        String sql =
            "SELECT bank, COUNT(*) AS freq FROM (" +
            "  SELECT UNNEST(STRING_TO_ARRAY(banks, ', ')) AS bank " +
            "  FROM p2p_ads " +
            "  WHERE timestamp::timestamp >= NOW() - INTERVAL '" + WINDOW + "'" +
            ") sub GROUP BY bank ORDER BY freq DESC LIMIT 1";

        try (Connection conn = db.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            if (rs.next()) {
                return rs.getString("bank");
            }
        }
        return "N/A";
    }
}
