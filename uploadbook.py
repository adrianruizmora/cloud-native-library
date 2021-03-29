import sys
import argparse
import configparser
import logging
import os.path
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
import mysql.connector
import os


config_sql = {
  'host':os.environ['HOST_SQL_AZURE'],
  'user':os.environ['USER_SQL_AZURE'],
  'password':os.environ['PASSWORD_SQL_AZURE'],
  'database':os.environ['DATABASE_SQL_AZURE'],
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': os.environ["SSL_CA_SQL_AZURE"]}


def list_blob(args, containerclient):
    """ 
    This function print on console all name of 
    blobs in the container.

    args : is the argument 'list'.

    container : is the container when you want see
    list of blobs.
    """
    logging.debug("Start function list_blob, we want to have all list of blobs")
    blob_list=containerclient.list_blobs()
    #configure the variable for return all blobs in container
    logging.info(f"list of blobs in container")

    for blob in blob_list:
        print(blob.name)
    logging.info(f"list of blobs in container")



def upload(cible, blobclient):
    """
    This function upload  file on the container
    the file on the container is a blob.

    cible : is the path of the file want to upload.

    blobclient : is the config for connect to azure.

    """
    with open(cible, "rb") as f:
        logging.warning("Upload blob in the container")
        blobclient.upload_blob(f)
        logging.info(f"Upload {f}done")



def main(args,config):
    """
    This function connect to azure if the application run
    with argument. with argument "upload" we uploading a file
    in the container, with argument "list" we have a list of
    all blobs is in the container
    """
    blobclient=BlobServiceClient(
        f"https://{config['storage']['account']}.blob.core.windows.net",
        config["storage"]["key"],
        logging_enable=False)
    logging.debug(f"account : {blobclient}")
    containerclient=blobclient.get_container_client(config["storage"]["container"])
    logging.debug(f"container : {containerclient}")
    if args.action=="list":
        logging.debug(f"account : {blobclient}")
        logging.debug("start of argument list we return function list_blob")
        return list_blob(args, containerclient)
        logging.info(f"{list_blob(args,containerclient)}")
        logging.debug(f"account : {blobclient}")

    else:
        if args.action=="upload":
            blobclient=containerclient.get_blob_client(os.path.basename(args.cible))
            print("Connection established")
            conn = mysql.connector.connect(**config_sql)
            cursor = conn.cursor()
            book_title = input("Quel est le titre de votre livre :")
            book_info = input("Quel est le genre de livre :")
            blob_url= f'https://cloudlibrary2.blob.core.windows.net/library/{book_title}.txt'
            cursor.execute("""INSERT INTO library (titre,info,urlblob) VALUES (%s, %s,%s)"""
                           ,(book_title,book_info,blob_url))
            conn.commit()
            logging.debug(f"Udapte file on container client : {blobclient} ")
            return upload(args.cible, blobclient)
            logging.info(f"The file {upload(args.cible,blobclient)}has been add on container")


if __name__=="__main__":
    parser=argparse.ArgumentParser("Logiciel d'uploap livre dans un container Azure")
    parser.add_argument("-cfg",default="config.ini",help="chemin du fichier de configuration")
    parser.add_argument("-lvl",default = "info", help="niveau de log")
    subparsers=parser.add_subparsers(dest="action",help="type d'operation")
    subparsers.required=True
    
    parser_s=subparsers.add_parser("upload")
    parser_s.add_argument("cible",help="fichier à envoyer")

    parser_r=subparsers.add_parser("list")

    args=parser.parse_args()

    loglevels={
    "debug":logging.DEBUG,
    "info":logging.INFO,
    "warning":logging.WARNING,
    "error":logging.ERROR,
    "critical":logging.CRITICAL
    }
    print(loglevels[args.lvl.lower()])
    print(f" lvl of logging = {[args.lvl.lower()]}")
    logging.basicConfig(level=loglevels[args.lvl.lower()])
    config=configparser.ConfigParser()
    config.read(args.cfg)

    sys.exit(main(args,config))
