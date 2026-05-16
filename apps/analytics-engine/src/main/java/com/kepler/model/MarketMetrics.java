package com.kepler.model;

/**
 * DTO that stores aggregated market metrics for a specific trade side (BUY or SELL).
 */
public class MarketMetrics {

    private String timestamp;
    private String tradeType;
    private double avgPrice;
    private double medianPrice;
    private double stdDev;
    private double priceRange;
    private int recordCount;

    // ── Getters ──────────────────────────────────────────────────────────────

    public String getTimestamp()    { return timestamp; }
    public String getTradeType()    { return tradeType; }
    public double getAvgPrice()     { return avgPrice; }
    public double getMedianPrice()  { return medianPrice; }
    public double getStdDev()       { return stdDev; }
    public double getPriceRange()   { return priceRange; }
    public int getRecordCount()     { return recordCount; }

    // ── Setters ──────────────────────────────────────────────────────────────

    public void setTimestamp(String timestamp)       { this.timestamp = timestamp; }
    public void setTradeType(String tradeType)       { this.tradeType = tradeType; }
    public void setAvgPrice(double avgPrice)         { this.avgPrice = avgPrice; }
    public void setMedianPrice(double medianPrice)   { this.medianPrice = medianPrice; }
    public void setStdDev(double stdDev)             { this.stdDev = stdDev; }
    public void setPriceRange(double priceRange)     { this.priceRange = priceRange; }
    public void setRecordCount(int recordCount)      { this.recordCount = recordCount; }

    @Override
    public String toString() {
        return String.format("MarketMetrics{tradeType='%s', avg=%.2f, median=%.2f, stdDev=%.2f, range=%.2f, count=%d}",
            tradeType, avgPrice, medianPrice, stdDev, priceRange, recordCount);
    }
}
