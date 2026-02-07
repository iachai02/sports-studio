from fastapi import FastAPI

def create_app():
    app = FastAPI()

    @app.get("/api/v1/health")
    def health():
        return {"status": "healthy"}
    
    return app