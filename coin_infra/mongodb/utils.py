from pymongo import MongoClient

def get_client():
    uri = "mongodb+srv://coin-time-series.rvdyfea.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = MongoClient(uri, tls=True,
                         tlsCertificateKeyFile='/home/yite/coin-infra/credential/X509-cert-1230238510090228621.pem')
    return client



