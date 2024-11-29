# Changelog

## [Unreleased]

### Added

- Added debug statements to `db_manager.py` to print connection parameters and SQL commands being executed.
- Updated `visualization.py` to ensure the `data` parameter is always a DataFrame in the `create_daily_trip_mileage_chart` function.

### Changed

- Updated `README.md` to reflect recent changes.

### Removed

- None

### Fixed

- Fixed `AttributeError` related to the `empty` method in `visualization.py`.
