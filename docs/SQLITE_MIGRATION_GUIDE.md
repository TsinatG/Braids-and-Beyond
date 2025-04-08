# SQLite Migration Guide for Braids & Beyond

This document provides guidance on working with SQLite migrations in the Braids & Beyond project. We've switched from MySQL to SQLite to simplify development and deployment.

## Current Database Structure

The application has four main models/tables:

1. **Client**: User accounts and authentication
2. **Stylist**: Information about hair stylists
3. **Service**: Available hair services with pricing
4. **Appointment**: Booking information connecting clients, stylists, and services

## Working with Migrations

SQLite has some limitations compared to other databases when it comes to schema changes. The most important one is that SQLite doesn't fully support `ALTER TABLE` statements for changing or dropping columns.

### Creating New Migrations

When you need to create a new migration:

```bash
flask db migrate -m "Description of your changes"
```

The migration will be generated in `migrations/versions/`. Always review the generated migration to ensure it's correct.

### Applying Migrations

To apply migrations to your database:

```bash
flask db upgrade
```

### SQLite-Specific Considerations

1. **Batch Mode**: We've configured Alembic to use batch mode for SQLite, which wraps schema changes in a sequence of steps that SQLite can handle.

2. **Foreign Keys**: We've explicitly enabled foreign key constraints in SQLite (they're disabled by default).

3. **Data Types**: SQLite uses a more flexible type system than MySQL. Be aware that:
   - `INTEGER PRIMARY KEY` in SQLite auto-increments (similar to MySQL's AUTO_INCREMENT)
   - Date/time values are stored as strings or integers
   - SQLite is more permissive about data types in general

## Troubleshooting Migration Issues

### If a migration fails:

1. Check the error message to understand what's happening.
2. For complex column changes, you might need to:
   - Create a new table with the desired structure
   - Copy data from the old table to the new one
   - Drop the old table
   - Rename the new table to the original name

### Common SQLite Migration Errors

1. **"no such column"**: This often occurs when trying to reference a column that doesn't exist yet. Ensure your migration order is correct.

2. **"table already exists"**: SQLite batch operations sometimes have issues with temporary tables. You might need to manually adjust the migration.

3. **"foreign key constraint failed"**: Check if you're trying to delete or modify a record that's referenced by other tables.

## Converting Existing Data

If you need to convert data from MySQL to SQLite, refer to the "Migrating from MySQL to SQLite" section in the README.md file.

## Backup Recommendations

SQLite stores the entire database in a single file, making backups straightforward:

```bash
# Simple file copy backup
cp braids_beyond.db braids_beyond.db.backup

# Or using sqlite3 command
sqlite3 braids_beyond.db .dump > backup.sql
```

## Performance Optimizations

We've applied several SQLite optimizations to improve performance in our application:

1. **Write-Ahead Logging (WAL)**: Enables better concurrency by allowing readers to continue while a writer is active
   ```sql
   PRAGMA journal_mode=WAL;
   ```

2. **Synchronous Mode**: Reduced to NORMAL to improve write performance while maintaining reasonable safety
   ```sql
   PRAGMA synchronous=NORMAL;
   ```

3. **Cache Size**: Increased to improve performance for frequently accessed data
   ```sql
   PRAGMA cache_size=10000;
   ```

4. **Temporary Storage**: Set to use memory for temporary tables and indices
   ```sql
   PRAGMA temp_store=MEMORY;
   ```

These optimizations are automatically applied when the application starts. If you're experiencing performance issues with large datasets or high concurrency, you might need to adjust these settings.

## Database Management Tools

Since SQLite doesn't have a built-in admin panel like phpMyAdmin for MySQL, we recommend using one of these tools:

1. **DB Browser for SQLite**: A visual tool for managing SQLite databases
   - Download from: https://sqlitebrowser.org/

2. **SQLite Studio**: Another excellent visual database manager
   - Download from: https://sqlitestudio.pl/

3. **VSCode Extensions**: If you use Visual Studio Code, install the "SQLite" extension 