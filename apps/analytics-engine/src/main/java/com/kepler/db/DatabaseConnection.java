package com.kepler.db;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * Provides JDBC connections to the PostgreSQL database.
 * Configuration is read from environment variables injected by Docker Compose.
 */
public class DatabaseConnection {

    private static final Logger log = LoggerFactory.getLogger(DatabaseConnection.class);

    private final String url;
    private final String user;
    private final String password;

    public DatabaseConnection() {
        String host = System.getenv().getOrDefault("DB_HOST", "localhost");
        String port = System.getenv().getOrDefault("DB_PORT", "5432");
        String name = System.getenv().getOrDefault("DB_NAME", "kepler");
        this.user     = System.getenv().getOrDefault("DB_USER", "kepler");
        this.password = System.getenv().getOrDefault("DB_PASS", "");
        this.url      = String.format("jdbc:postgresql://%s:%s/%s", host, port, name);
        log.info("Database configured: {}", url);
    }

    /**
     * Opens and returns a new JDBC connection.
     * Callers are responsible for closing the connection (use try-with-resources).
     */
    public Connection getConnection() throws SQLException {
        return DriverManager.getConnection(url, user, password);
    }
}
