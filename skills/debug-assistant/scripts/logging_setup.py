import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Usage:
# logger.debug("_save_turn called: role=%s", role)
# logger.info("Profile updated for user %s", user_id)
# logger.warning("JSON parse failed, retrying: %s", e)
# logger.error("Tool handler missing for %s", name)
