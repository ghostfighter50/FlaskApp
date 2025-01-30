# run.py

import logging
from app import create_app

def main() -> None:
    """
    Entry point for the Flask application.
    Initializes and runs the Flask app.
    """
    app = create_app()

    # Configure logging for the run script
    logging.basicConfig(level=logging.INFO)
    app.logger.info("Starting Flask application.")
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()
