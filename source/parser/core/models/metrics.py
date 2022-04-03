from parser.core.models.model import Model
from parser.core.db.connections import Connections

class Metrics(Model):
    
    table = 'metrics'

    hirarchy = None

    def set_parent(self, id):
        cn = Connections()
        if self.hirarchy is None:
            q = "INSERT INTO `metrics_hirarchy` (s_title, metric, parent)" + \
                " VALUES(%s, %s, %s)"
            iq = cn.query_insert(q, (self.get('s_title'), self.id, id))
        else:
            if self.hirarchy['parent'] == id:
                return self
            q = "UPDATE `metrics_hirarchy` SET `parent` = %s WHERE `metric` = %s"
            cn.query_insert(q, (id, self.id))
        self.load_hirarchy()
        return self

    def load_hirarchy(self):
        cn = Connections()
        q = "SELECT * FROM `metrics_hirarchy` WHERE `metric` = %s"
        self.hirarchy = cn.query_single(q, (self.id))
        return self

    def after_load(self):
        self.load_hirarchy()
        return self

    
        