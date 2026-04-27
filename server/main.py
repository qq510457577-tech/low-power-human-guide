import json
import os
import uuid
import uvicorn
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

# --- Constants ---
WG_PASSWORD = os.environ.get("WG_PASSWORD", "changeme")
from pydantic import BaseModel
import httpx

app = FastAPI(title="人类低功耗生存指南 API", version="1.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Breast Cancer API ---
from breast_cancer_api import router as breast_cancer_router
app.include_router(breast_cancer_router)

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
SHARES_FILE = DATA_DIR / "shares.json"
FRONTEND_DIR = BASE_DIR.parent / "dist"  # Vite build output
WIREGUARD_DIR = Path("/root/wireguard/www")

# DeepSeek
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

# ---------------------- Data Layer ----------------------

def load_shares():
    if not SHARES_FILE.exists():
        return []
    with open(SHARES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_shares(shares):
    with open(SHARES_FILE, "w", encoding="utf-8") as f:
        json.dump(shares, f, ensure_ascii=False, indent=2)

# ---------------------- API Routes ----------------------

class ExtractRequest(BaseModel):
    content: str

class ShareRequest(BaseModel):
    title: str
    content: str
    points: list[str]

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "人类低功耗生存指南 API",
        "version": "1.1.0",
        "has_deepseek_key": bool(DEEPSEEK_API_KEY)
    }

@app.post("/api/extract")
async def extract(req: ExtractRequest):
    if not req.content or len(req.content.strip()) < 5:
        raise HTTPException(400, "心得内容至少5个字符")
    
    if not DEEPSEEK_API_KEY:
        # Fallback: keyword extraction
        return _fallback_extract(req.content)
    
    prompt = f"""你是一个禅意生活导师。请从以下用户心得中提炼出3-5条核心要点，并给出一句话总结。

要求：
- 每条要点用6字以内精炼概括，风格简洁有禅意
- 一句话总结控制在12字以内
- 直接输出JSON，不要任何其他内容

用户心得：{req.content}

输出格式：{{"points": ["要点1", "要点2", "要点3"], "summary": "一句话总结"}}"""

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(DEEPSEEK_URL, json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 300
            }, headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            })
            resp.raise_for_status()
            data = resp.json()
            result = json.loads(data["choices"][0]["message"]["content"])
            return {"points": result["points"], "summary": result["summary"]}
    except Exception as e:
        return _fallback_extract(req.content)

def _fallback_extract(content: str):
    """Simple fallback when DeepSeek is unavailable."""
    sentences = [s.strip() for s in content.replace("。", "。\n").split("\n") if len(s.strip()) > 6]
    points = sentences[:4] if sentences else [content[:20]]
    summary = content[:20] + "..." if len(content) > 20 else content
    return {"points": points, "summary": summary}

@app.post("/api/share")
def create_share(req: ShareRequest):
    shares = load_shares()
    share = {
        "id": str(uuid.uuid4()),
        "title": req.title,
        "content": req.content,
        "points": req.points,
        "likes": 0,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    shares.insert(0, share)
    save_shares(shares)
    return {"id": share["id"], "message": "发布成功"}

@app.get("/api/share")
def list_shares():
    shares = load_shares()
    shares.sort(key=lambda s: s.get("likes", 0), reverse=True)
    return shares

@app.get("/api/share/{share_id}")
def get_share(share_id: str):
    shares = load_shares()
    for share in shares:
        if share["id"] == share_id:
            return share
    raise HTTPException(404, "分享不存在")

@app.post("/api/share/{share_id}/like")
def like_share(share_id: str):
    shares = load_shares()
    for share in shares:
        if share["id"] == share_id:
            share["likes"] = share.get("likes", 0) + 1
            save_shares(shares)
            return {"likes": share["likes"]}
    raise HTTPException(404, "分享不存在")

# ---------------------- Static File Serving ----------------------

# Mount wireguard pages at /wireguard with password protection
if WIREGUARD_DIR.exists():
    def check_wg_auth(auth: str = None):
        if not auth or not auth.startswith("Basic "):
            return False
        import base64
        try:
            decoded = base64.b64decode(auth[6:]).decode("utf-8")
            _, password = decoded.split(":", 1)
            return password == WG_PASSWORD
        except:
            return False

    def wg_auth_required(authorization: str = None):
        if not check_wg_auth(authorization):
            from fastapi.responses import Response
            return Response(
                content="<html><body><h1>401 Unauthorized</h1><p>请输入密码访问 WireGuard 管理页面</p></body></html>",
                status_code=401,
                headers={"WWW-Authenticate": 'Basic realm="WireGuard VPN"'},
                media_type="text/html"
            )
        return None

    @app.get("/wireguard")
    @app.get("/wireguard/")
    @app.get("/wireguard_complete.html")
    async def wireguard_page(authorization: str = Header(None)):
        auth_result = wg_auth_required(authorization)
        if auth_result:
            return auth_result
        
        idx = WIREGUARD_DIR / "index.html"
        if idx.exists():
            return FileResponse(str(idx))
        return {"error": "WireGuard page not found"}
    
    # Serve static files under /wireguard/ with auth
    @app.get("/wireguard/{file_path:path}")
    async def wireguard_static(file_path: str, authorization: str = Header(None)):
        auth_result = wg_auth_required(authorization)
        if auth_result:
            return auth_result
        file = WIREGUARD_DIR / file_path
        if file.exists() and file.is_file():
            return FileResponse(str(file))
        return {"error": "File not found"}

# Portal entry page
PORTAL_FILE = BASE_DIR / "portal.html"

@app.get("/")
async def portal():
    portal = PORTAL_FILE
    if portal.exists():
        return FileResponse(str(portal))
    return {"message": "服务入口"}

# Breast cancer frontend page
BREAST_CANCER_FILE = BASE_DIR / "static" / "breast_cancer.html"

@app.get("/breast-cancer")
@app.get("/breast-cancer/")
async def breast_cancer_page():
    bc = BREAST_CANCER_FILE
    if bc.exists():
        return FileResponse(str(bc))
    return {"error": "Breast cancer page not found"}

# Serve frontend static files (Vite build) at /low-power-human-guide/
if FRONTEND_DIR.exists():
    app.mount("/low-power-human-guide/assets", StaticFiles(directory=str(FRONTEND_DIR / "assets")), name="assets_lowpower")
    
    @app.get("/low-power-human-guide/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = FRONTEND_DIR / (full_path or "index.html")
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        index = FRONTEND_DIR / "index.html"
        if index.exists():
            return FileResponse(str(index))
        return {"error": "Frontend not built"}

# ---------------------- Entry ----------------------

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
