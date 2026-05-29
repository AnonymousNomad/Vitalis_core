import logging
from vitalis.src.core.heartbeat_loop import HeartbeatLoop
from vitalis.src.brain.brain_interface import VitalisBrain

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Supervisor")

def run_supervisor():
    logger.info("Initializing Ferrell Synthetic Intelligence Supervisor...")
    
    # Instantiate the correct class
    brain = VitalisBrain()
    
    # Inject the brain dependency
    loop = HeartbeatLoop(brain=brain)
    
    try:
        logger.info("Starting persistent heartbeat loop...")
        loop.start()
    except KeyboardInterrupt:
        logger.info("Supervisor shut down by operator.")

if __name__ == "__main__":
    run_supervisor()
