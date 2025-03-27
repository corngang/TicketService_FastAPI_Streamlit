import configparser
import uvicorn
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse

config = configparser.ConfigParser()
config.read('/TicketService_FastAPI_Streamlit/cognito_split/fastapi/cognito.ini')

COGNITO_DOMAIN = os.getenv("RESERVE_URL", config['COGNITO']['COGNITO_DOMAIN'])
CLIENT_ID = os.getenv("CLIENT_ID", config['COGNITO']['CLIENT_ID'])
CLIENT_SECRET = os.getenv("CLIENT_SECRET", config['COGNITO']['CLIENT_SECRET'])
APP_URI = os.getenv("APP_URI", config['COGNITO']['APP_URI'])

# 환경 변수로 호스트와 포트를 설정
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", 8001))

app = FastAPI()
############################2929292929#############################
