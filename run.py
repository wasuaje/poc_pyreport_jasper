# Boiler plate stuff to start the module
import pathlib
import jpype
import jpype.imports
from jpype.types import *
import os
from pyreportjasper import PyReportJasper, config, report
from functools import lru_cache
from dotenv import load_dotenv
load_dotenv()
# Launch the JVM
# jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=jars/mysql-connector-java-8.0.29.jar")
# nopep8
# from java.lang import System

# print(System.getProperty('java
# .class.path'))
# import the Java classes

# import the Java modules
# from com.paying.customer import DataBase
user = os.environ.get('mysql_user', '')
passw = os.environ.get('mysql_pass', '')
host = os.environ.get('mysql_host', '')
db = os.environ.get('mysql_db_name', '')


JDBC_PATH = os.path.join(pathlib.Path().resolve(), "jars")
jdbc_path = os.path.join(JDBC_PATH, 'mysql-connector-java-8.0.29.jar')
REPORTS_DIR = "reports/"

db_report_connection = {
    'driver': 'mysql',
    'host': host,
    'port': 3306,
    'database': db,
    'username': user,
    'password': passw,
    'jdbc_driver': "com.mysql.cj.jdbc.Driver",
    'jdbc_dir': jdbc_path
}


@lru_cache(maxsize=128)
def get_products_report():
    file_type = 'pdf'
    if file_type is not None:
        file_type = file_type.lower()
    else:
        file_type = 'pdf'
    input_file = os.path.join(REPORTS_DIR, 'rptProducts.jasper')
    output_file = os.path.join(REPORTS_DIR, 'ProductsReport')
    # logo_path = get_config_value(db, 'company_static_url')
    # logo_path += '/img/logo.png'

    # pyreportjasper = PyReportJasper()
    # pyreportjasper.config(
    #     input_file,
    #     output_file,
    #     locale='es_AR',
    #     output_formats=[file_type],
    #     parameters={
    #         'image_path': '',
    #         'company_name':  'company_name'},
    #     db_connection=db_report_connection
    # )
    # pyreportjasper.process_report()
    m_config = config.Config()
    m_config.input = input_file
    m_config.output = output_file
    m_config.locale = 'es_AR'
    m_config.outputFormats = [file_type]
    m_config.params = {
        'image_path': '',
        'company_name':  'company_name'}
    m_config.dbHost = db_report_connection['host']
    m_config.dbType = 'mysql'
    m_config.jvm_maxmem = '4096m'
    m_config.dbPort = db_report_connection['port']
    m_config.dbName = db_report_connection['database']
    m_config.dbUser = db_report_connection['username']
    m_config.dbPasswd = db_report_connection['password']
    m_config.dbDriver = db_report_connection['jdbc_driver']
    m_config.jdbcDir = db_report_connection['jdbc_dir']


    m_report = report.Report(m_config, input_file=input_file)
    m_report.fill_internal()
    # print("Exporting to PDF", m_report.get_main_dataset_query())
    # classmethodget_output_stream = m_report.get_output_stream('suffix')

    # with open('myrepor.pdf', 'wb') as f:
        # f.write(classmethodget_output_stream)
    # print("Exporting to PDF", classmethodget_output_stream)
    m_report.export_pdf()

    return output_file+"."+file_type


def get_products_report_csv():
    file_type = 'pdf'
    if file_type is not None:
        file_type = file_type.lower()
    else:
        file_type = 'pdf'
    input_file = os.path.join(REPORTS_DIR, 'rptProducts.jasper')
    output_file = os.path.join(REPORTS_DIR, 'ProductsReport')
    conn = {
        'driver': 'csv',
        'data_file': 'data.csv',
        'csv_charset': 'utf-8',
        'csv_out_charset': 'utf-8',
        'csv_field_del': ',',
        'csv_out_field_del': ',',
        'csv_record_del': "\n",
        'csv_first_row': True,
        'csv_columns': "cat_id,cat_name,code,prod_name,format,price,cost,stock".split(",")
    }
    pyreportjasper = PyReportJasper()
    pyreportjasper.config(
        input_file,
        output_file,
        output_formats=["pdf"],
        db_connection=conn
    )
    pyreportjasper.process_report()
    print('Result is the file below.')
    print(output_file + '.pdf')


# Launch the JVM
# jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=jars/*")
import cProfile
# cProfile.run('get_products_report()', sort='tottime')
# cProfile.run('get_products_report_csv()', sort='tottime')
get_products_report_csv()

# nopep8
# import java.lang
# from java.lang import System
# from org.pkg.MyClassPackage import MyClass

# print(System.getProperty('java.class.path'))
