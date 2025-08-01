import uvicorn
from api.app import app  # Adjust the import path to match your app location

if __name__ == "__main__":
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)
