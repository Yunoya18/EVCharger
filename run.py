from User_Package import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="", port=8000)
