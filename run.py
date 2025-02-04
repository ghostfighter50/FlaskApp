import logging
from app import create_app
from waitress import serve

def main() -> None:
    app = create_app()

    logging.basicConfig(level=logging.INFO)
    app.logger.info("Starting Flask application.")
    serve(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
