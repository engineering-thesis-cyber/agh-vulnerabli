import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(levelname)s][%(filename)s] - %(message)s",
)
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(
    logging.Formatter("[%(asctime)s][%(levelname)s][%(filename)s] - %(message)s")
)
l = logging.getLogger(__name__)
l.addHandler(file_handler)
