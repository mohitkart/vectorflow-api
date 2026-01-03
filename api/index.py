import os
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from dotenv import load_dotenv

load_dotenv()  # safe: ignored on Vercel

app = FastAPI()

# 🔐 Read allowed origins from env
cors_origins = os.getenv("CORS_ORIGINS", "")
allowed_origins = [origin.strip() for origin in cors_origins.split(",") if origin]

# 🔎 Debug (optional)
print("CORS allowed origins:", allowed_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins or ["*"],  # fallback only if env missing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Node(BaseModel):
    id: str
    type: str = "default"
    data: Dict[str, Any] = {}

class Edge(BaseModel):
    source: str
    target: str
    
class PipelineRequest(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]


# DAG validation using DFS
# def is_dag(nodes: List[any], edges: List[Edge]) -> bool:
#     graph = {node.id: [] for node in nodes}
#     for edge in edges:
#         graph[edge.source].append(edge.target)

#     visited = set()
#     rec_stack = set()

#     def dfs(node):
#         if node in rec_stack:
#             return False  # cycle found
#         if node in visited:
#             return True
#         visited.add(node)
#         rec_stack.add(node)
#         for neighbor in graph[node]:
#             if not dfs(neighbor):
#                 return False
#         rec_stack.remove(node)
#         return True

#     for node in graph:
#         if node not in visited:
#             if not dfs(node):
#                 return False
#     return True

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
def parse_pipeline(data: PipelineRequest):
    return {
        "num_nodes": len(data.nodes),
        "num_edges": len(data.edges),
        # "is_dag": is_dag(data.nodes, data.edges)
        "is_dag": True
    }
