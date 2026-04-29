from iot_soc_api.app import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("iot_soc_api.app:app", host="127.0.0.1", port=8766, reload=False)
