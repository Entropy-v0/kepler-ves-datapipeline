package com.kepler.model;

/**
 * POJO representing a single P2P advertisement row from the p2p_ads table.
 * Field names match the column names produced by Kepler's processor.
 */
public class AdvertP2P {

    private String timestamp;
    private String tradeType;   // "BUY" or "SELL"
    private String fiat;        // e.g. "VES"
    private int    page;
    private String merchant;
    private String banks;
    private double price;
    private double minLimit;
    private double maxLimit;
    private double available;
    private int    orders;
    private double successRate;

    // ── Getters ──────────────────────────────────────────────────────────────

    public String getTimestamp()   { return timestamp; }
    public String getTradeType()   { return tradeType; }
    public String getFiat()        { return fiat; }
    public int    getPage()        { return page; }
    public String getMerchant()    { return merchant; }
    public String getBanks()       { return banks; }
    public double getPrice()       { return price; }
    public double getMinLimit()    { return minLimit; }
    public double getMaxLimit()    { return maxLimit; }
    public double getAvailable()   { return available; }
    public int    getOrders()      { return orders; }
    public double getSuccessRate() { return successRate; }

    // ── Setters ──────────────────────────────────────────────────────────────

    public void setTimestamp(String timestamp)     { this.timestamp = timestamp; }
    public void setTradeType(String tradeType)     { this.tradeType = tradeType; }
    public void setFiat(String fiat)               { this.fiat = fiat; }
    public void setPage(int page)                  { this.page = page; }
    public void setMerchant(String merchant)       { this.merchant = merchant; }
    public void setBanks(String banks)             { this.banks = banks; }
    public void setPrice(double price)             { this.price = price; }
    public void setMinLimit(double minLimit)       { this.minLimit = minLimit; }
    public void setMaxLimit(double maxLimit)       { this.maxLimit = maxLimit; }
    public void setAvailable(double available)     { this.available = available; }
    public void setOrders(int orders)              { this.orders = orders; }
    public void setSuccessRate(double successRate) { this.successRate = successRate; }

    @Override
    public String toString() {
        return String.format("AdvertP2P{tradeType='%s', merchant='%s', price=%.2f, available=%.2f}",
            tradeType, merchant, price, available);
    }
}
