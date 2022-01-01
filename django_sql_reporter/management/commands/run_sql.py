from django.core.management.base import BaseCommand
from django.db import connections
from django_sql_reporter.models import SQLResultReport
from django.core.mail import send_mail
from pathlib import Path
import glob
import yaml
import sys

from tests.testapp.settings import BASE_DIR

def dict_fetch_all(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class Command(BaseCommand):
    help = 'Execute SQL based on the yml configuration file.'

    def add_arguments(self, parser):  # コマンド引数の定義
        # int型の必須引数の定義
        parser.add_argument('dir_path', type=str, help='ymlファイルの格納先ディレクトリを指定してください。')
        print(BASE_DIR)

    def handle(self, *args, **kwargs):
        dir_path = kwargs['dir_path'];
        files = glob.glob(dir_path + "/*.yaml")

        is_failed = False
        with connections['sql_reporter_default'].cursor() as cursor:
            for file in files:
                print(f"Checking {file}...")

            with open(file, 'r') as yml:
                monitoring_items = yaml.safe_load(yml)
                for monitor in monitoring_items:
                    try:
                        query = monitor["sql"]
                        cursor.execute(query)
                        records = dict_fetch_all(cursor)

                        if records != monitor["expect"]:
                            is_failed = True

                            print("====================", file=sys.stderr)
                            print(f"Unexpected query result for {file}", file=sys.stderr)
                            print(f"Executed SQL:\n{query}", file=sys.stderr)
                            print(f"Expected result:\n{monitor['expect']}", file=sys.stderr)
                            print(f"Actual result:\n{records}", file=sys.stderr)

                            file_name = Path(file).name

                            # ステータス:送信中で保存
                            result = SQLResultReport(name=file_name, body=records, send_status=1)
                            result.save()

                            print("====================", file=sys.stderr)
                            print("sendmail start", file=sys.stderr)

                            send_mail(file_name, monitor["description"], "test@exeample.com", monitor["recipient_list"])
                            result.send_status = 2
                            result.save()

                        else:
                            file_name = Path(file).name
                            result = SQLResultReport(name=file_name, body=records, send_status=2)
                            result.save()

                    except Exception as e:
                            print(e, file=sys.stderr)

        if is_failed:
            sys.exit(1)
