from parser.core.db.connections import Connections

class Model:
    
    data: dict = {}
    primary_field = 'id'
    table: str

    def after_load(self):
        pass

    def load(self, id):
        cn = Connections()
        query = 'SELECT * FROM `%s` ' % self.table
        query += ('WHERE `%s` = '% self.primary_field) + '%s'
        rec = cn.query_single(query, (id))
        if rec is None:
            raise Exception("Can't load %s with %s = %s" % (self.table, self.primary_field, id))
        self.set_data(rec)
        self.after_load()
        return self

    def load_by_fields(self, fields: dict):
        cn = Connections()
        query = 'SELECT * FROM %s WHERE ' % self.table
        wh_item = []
        params = []
        for field in fields.keys():
            it = ("`%s` = " % field) + "%s"
            params.append(fields[field])
            wh_item.append(it)
        
        where = ' AND '.join(wh_item)
        query = query + where
        rec = cn.query_single(query, tuple(params))
        if rec is None:
            raise Exception("Can't load %s fields" % self.table)
        self.set_data(rec)
        self.after_load()
        return self

    def save(self):
        cn = Connections()
        if self.id is None:
            q ='INSERT INTO %s ' % self.table
            fields = ' ,'.join(self.data.keys())
            q += '(%s) ' % fields
            v = ['%s'] * len(self.data.keys())
            v = ', '.join(v)
            q += 'VALUES(%s)' % v
            last_id = cn.query_insert(q, tuple(self.data.values()))
            self.load(last_id['id'])
            return self
        else:
            pass

    def set_data(self, d:dict):
        self.data = d 
        return self

    def set_key(self, name, value):
        self.data[name] = value

    @property
    def id(self):
        return self.get('id')

    def get(self, name, default = None):
        if name in self.data:
            return self.data[name]
        return default