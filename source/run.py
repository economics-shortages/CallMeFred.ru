
from parser.core.db.connections import Connections
from parser.targets import Targets


tg = Targets()
tg.parse_targets()

db = Connections().query('SHOW TABLES');
print(db)
