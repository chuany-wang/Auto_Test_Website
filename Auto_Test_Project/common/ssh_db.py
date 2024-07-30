import asyncio
import pymysql
from common.init_sqlalchemy import db
from common.read_data import read_conf
from sshtunnel import SSHTunnelForwarder
from models.site.site_database_info import SiteDatabase
from config.site_config import envir_to_filter_map_database

SSH = read_conf('SSH')


class DatabaseManager:

    def __init__(self, ssh_username, ssh_password, ssh_host, ssh_port,
                 db_host, db_port, db_user, db_password, db_name,
                 charset='utf8'):
        self.server = SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_username,
            ssh_password=ssh_password,
            remote_bind_address=(db_host, db_port)
        )

        self.conn = None
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.charset = charset

    def __enter__(self):
        self.server.start()
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=self.server.local_bind_port,
            user=self.db_user,
            password=self.db_password,
            db=self.db_name,
            charset=self.charset,
        )
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        return self

    def execute(self, sql):
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()
        self.server.stop()


def get_db_info(site_host=None, envir=None):
    if site_host:
        query = db.query(SiteDatabase).filter_by(site_host=site_host).first()
    else:
        filter_condition_key = envir_to_filter_map_database.get(envir, lambda: SiteDatabase.site_id >= 3000)()
        query = db.query(SiteDatabase).filter(filter_condition_key).all()

    return query


async def process_site(site, sql):
    with DatabaseManager(
            ssh_username=SSH.get('ssh_username'),
            ssh_password=SSH.get('ssh_password'),
            ssh_host=SSH.get('ssh_host'),
            ssh_port=int(SSH.get('ssh_port')),
            db_host=site.pro_host,
            db_port=3306,
            db_user=site.user,
            db_password=site.password,
            db_name=site.pro_db
    ) as db_manager:
        res = db_manager.execute(sql)
    return site.site_host, res


async def run_site(sql, envir):
    sites = get_db_info(envir=envir)
    tasks = [process_site(site, sql) for site in sites]
    results = await asyncio.gather(*tasks)
    return results


def get_all_site_data_from_db(sql, envir=None):
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(run_site(sql, envir))
    return result


def get_one_site_data_from_db(site_host, sql):
    site = get_db_info(site_host=site_host)
    with DatabaseManager(
            ssh_username=SSH.get('ssh_username'),
            ssh_password=SSH.get('ssh_password'),
            ssh_host=SSH.get('ssh_host'),
            ssh_port=int(SSH.get('ssh_port')),
            db_host=site.pro_host,
            db_port=3306,
            db_user=site.user,
            db_password=site.password,
            db_name=site.pro_db
    ) as db_manager:
        res = db_manager.execute(sql)
    return res


if __name__ == '__main__':
    x = get_all_site_data_from_db('SELECT language_id,`name`,`code`,`status` FROM `oc_language`')
    print(x)
