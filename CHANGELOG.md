# Changelog

## [Unreleased]
### Added
- Updated `pdf_parser.py` to use LangChain for PDF extraction, utilizing a LangChain agent to extract the required trip data from PDF files as a list of records.
- Updated `.env` file to include new OpenAI-related keys while preserving the existing keys for InfluxDB, PostgreSQL, and Authentik credentials, including the client ID and client secret for Authentik.
- Updated `db_manager.py` to include the necessary imports and ensure that the environment variables are loaded correctly while preserving the existing code.

## [1.0.0] - 2023-10-01
### Added
- Initial release of the project.
