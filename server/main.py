"""
人类低功耗生存指南 - 后端 API 服务
FastAPI 应用，提供心得提炼、分享存储、点赞等功能
"""

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── 路径 ──────────────────────────────────────────────
DATA_DIR = Path(__file__).parent / "data"
SHARES_FILE = DATA_DIR / "shares.json"

# ── 应用 ──────────────────────────────────────────────
app = FastAPI(title="人类低功耗生存指南 API", version="1.0.0")

# CORS - 允许 GitHub Pages 等跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://clawdlc.github.io",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://43.133.192.17:8888",
    ],
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── DeepSeek ──────────────────────────────────────────
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"


# ── 数据 ──────────────────────────────────────────────
def _load_shares() -> list[dict]:
    if not SHARES_FILE.exists():
        return []
    with open(SHARES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_shares(shares: list[dict]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(SHARES_FILE, "w", encoding="utf-8") as f:
        json.dump(shares, f, ensure_ascii=False, indent=2)


# ── 请求/响应模型 ─────────────────────────────────────
class ExtractRequest(BaseModel):
    content: str


class ExtractResponse(BaseModel):
    points: list[str]
    summary: str


class ShareCreate(BaseModel):
    title: str
    content: str
    points: list[str]


class LikeResponse(BaseModel):
    id: str
    likes: int


# ── 路由 ──────────────────────────────────────────────


@app.post("/api/extract")
async def extract(req: ExtractRequest):
    """
    用户心得 → AI提炼 3-5 条核心要点
    调用 DeepSeek API，prompt 为禅意极简风格
    """
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="心得内容不能为空")

    if not DEEPSEEK_API_KEY:
        # 降级：简单关键词提取
        return _fallback_extract(req.content)

    system_prompt = (
        "你是一位深谙低功耗生活之道的禅意导师。"
        "用户会分享一段关于健康生活、极简主义、冥想、运动、欲望管理等方面的心得体会。"
        "请静心品读，从中提炼出 3-5 条最核心的智慧要点。\n\n"
        "要求：\n"
        "- 每一条要点须精炼克制，15字以内\n"
        "- 语气如禅语，点到即止\n"
        "- 最后给出 20 字以内的一句话总结\n"
        "- 仅返回 JSON，格式如下：\n"
        '{"points": ["要点1", "要点2", ...], "summary": "一句话总结"}'
    )

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.content},
        ],
        "temperature": 0.3,
        "max_tokens": 500,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            DEEPSEEK_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            },
            json=payload,
        )

    if resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"DeepSeek API 调用失败: {resp.status_code}",
        )

    data = resp.json()
    text = data.get("choices", [{}])[0].get("message", {}).get("content", "")

    # 尝试解析 JSON
    try:
        result = json.loads(text)
        points = result.get("points", [])
        summary = result.get("summary", "")
    except (json.JSONDecodeError, TypeError):
        points = _parse_fallback(text)
        summary = ""

    # 兜底
    if not points:
        points = ["无法自动提炼，请手动编辑"]

    return {"points": points[:5], "summary": summary[:40]}


@app.post("/api/share")
async def create_share(req: ShareCreate):
    """提交一条分享"""
    if not req.title.strip():
        raise HTTPException(status_code=400, detail="标题不能为空")

    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")

    record = {
        "id": str(uuid.uuid4()),
        "标题": req.title,
        "内容": req.content,
        "提炼要点": req.points,
        "点赞数": 0,
        "创建时间": now,
    }

    shares = _load_shares()
    shares.insert(0, record)  # 最新在前
    _save_shares(shares)

    return {"id": record["id"], "message": "发布成功"}


@app.get("/api/share")
async def list_shares():
    """获取所有分享，按点赞数降序"""
    shares = _load_shares()
    shares.sort(key=lambda s: s.get("点赞数", 0), reverse=True)
    return shares


@app.post("/api/share/{share_id}/like")
async def like_share(share_id: str):
    """为分享点赞"""
    shares = _load_shares()
    for s in shares:
        if s.get("id") == share_id:
            s["点赞数"] = s.get("点赞数", 0) + 1
            _save_shares(shares)
            return {"id": share_id, "likes": s["点赞数"]}

    raise HTTPException(status_code=404, detail="分享不存在")


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "人类低功耗生存指南 API"}


# ── 辅助函数 ──────────────────────────────────────────


def _fallback_extract(content: str) -> dict:
    """无 API Key 时的降级方案"""
    lines = [l.strip() for l in content.split("\n") if l.strip()]
    # 取前5行作为要点
    points = [l[:20] for l in lines[:5]]
    if not points:
        points = ["请手动编辑要点"]
    summary = content[:30] + "…" if len(content) > 30 else content
    return {"points": points[:5], "summary": summary}


def _parse_fallback(text: str) -> list[str]:
    """非 JSON 响应时尝试解析文本"""
    lines = text.strip().split("\n")
    result = []
    for line in lines:
        clean = line.strip()
        if not clean:
            continue
        # 去掉常见序号前缀
        clean = clean.lstrip("0123456789.、-*#—").strip()
        if clean:
            result.append(clean)
    return result[:5]
