import uvicorn
from api.app import app  # Adjust the import path to match your app location

if __name__ == "__main__":
    uvicorn.run("api.app:app", host="127.0.0.1", port=8000, reload=True)
