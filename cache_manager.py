# cache_manager.py

import os
import json
import hashlib

CACHE_FILE = "pdf_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def get_pdf_key(file_path):
    # Hash PDF path for unique key
    return hashlib.md5(file_path.encode()).hexdigest()

def get_cached_summary(file_path):
    key = get_pdf_key(file_path)
    cache = load_cache()
    return cache.get(key, None)

def cache_summary(file_path, summary):
    key = get_pdf_key(file_path)
    cache = load_cache()
    cache[key] = summary
    save_cache(cache)
