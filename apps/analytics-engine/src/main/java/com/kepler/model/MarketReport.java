package com.kepler.model;

/**
 * Holds the computed market metrics for a single analysis cycle.
 */
public class MarketReport {

    private String timestamp;
    private double avgPriceBuy;
    private double avgPriceSell;
    private double spread;
    private double spreadPct;
    private double priceRangeBuy;
    private double priceRangeSell;
    private String topMerchantBuy;
    private String topMerchantSell;
    private String dominantBank;
    private int totalRecordsBuy;
    private int totalRecordsSell;

    // ── Getters ──────────────────────────────────────────────────────────────

    public String getTimestamp() {
        return timestamp;
    }

    public double getAvgPriceBuy() {
        return avgPriceBuy;
    }

    public double getAvgPriceSell() {
        return avgPriceSell;
    }

    public double getSpread() {
        return spread;
    }

    public double getSpreadPct() {
        return spreadPct;
    }

    public double getPriceRangeBuy() {
        return priceRangeBuy;
    }

    public double getPriceRangeSell() {
        return priceRangeSell;
    }

    public String getTopMerchantBuy() {
        return topMerchantBuy;
    }

    public String getTopMerchantSell() {
        return topMerchantSell;
    }

    public String getDominantBank() {
        return dominantBank;
    }

    public int getTotalRecordsBuy() {
        return totalRecordsBuy;
    }

    public int getTotalRecordsSell() {
        return totalRecordsSell;
    }

    // ── Setters ──────────────────────────────────────────────────────────────

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public void setAvgPriceBuy(double avgPriceBuy) {
        this.avgPriceBuy = avgPriceBuy;
    }

    public void setAvgPriceSell(double avgPriceSell) {
        this.avgPriceSell = avgPriceSell;
    }

    public void setSpread(double spread) {
        this.spread = spread;
    }

    public void setSpreadPct(double spreadPct) {
        this.spreadPct = spreadPct;
    }

    public void setPriceRangeBuy(double priceRangeBuy) {
        this.priceRangeBuy = priceRangeBuy;
    }

    public void setPriceRangeSell(double priceRangeSell) {
        this.priceRangeSell = priceRangeSell;
    }

    public void setTopMerchantBuy(String topMerchantBuy) {
        this.topMerchantBuy = topMerchantBuy;
    }

    public void setTopMerchantSell(String topMerchantSell) {
        this.topMerchantSell = topMerchantSell;
    }

    public void setDominantBank(String dominantBank) {
        this.dominantBank = dominantBank;
    }

    public void setTotalRecordsBuy(int totalRecordsBuy) {
        this.totalRecordsBuy = totalRecordsBuy;
    }

    public void setTotalRecordsSell(int totalRecordsSell) {
        this.totalRecordsSell = totalRecordsSell;
    }

    /**
     * Serializes this report to a CSV row.
     * Commas inside string fields are replaced with semicolons to avoid breaking
     * the format.
     */
    public String toCsvRow() {
        return String.format("%s,%.2f,%.2f,%.2f,%.3f,%.2f,%.2f,%s,%s,%s,%d,%d",
                timestamp,
                avgPriceBuy,
                avgPriceSell,
                spread,
                spreadPct,
                priceRangeBuy,
                priceRangeSell,
                topMerchantBuy.replace(",", ";"),
                topMerchantSell.replace(",", ";"),
                dominantBank.replace(",", ";"),
                totalRecordsBuy,
                totalRecordsSell);
    }
}
