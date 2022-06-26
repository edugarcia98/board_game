import logging


logging.basicConfig(
    filename="logger/results.log",
    filemode="w",
    level=logging.INFO,
    format=u"%(message)s",
    encoding="utf8",
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.addHandler(console)
