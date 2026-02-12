"""Hugging Face model info tool."""

import json
import sys
import urllib.request
import urllib.error


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m tools.hf_info <model_id>")
        print("Example: python -m tools.hf_info Qwen/Qwen3-TTS")
        sys.exit(1)

    model_id = sys.argv[1]
    url = f"https://huggingface.co/api/models/{model_id}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AI-Daily-Paper/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error: HTTP {e.code} for model '{model_id}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    pipeline = data.get("pipeline_tag", "unknown")
    downloads = data.get("downloads", 0)
    likes = data.get("likes", 0)
    last_modified = data.get("lastModified", "unknown")
    if last_modified != "unknown":
        last_modified = last_modified[:10]
    tags = ", ".join(data.get("tags", []))

    print(f"model: {model_id}")
    print(f"pipeline: {pipeline}")
    print(f"downloads: {downloads} | likes: {likes}")
    print(f"last_modified: {last_modified}")
    print(f"tags: {tags}")


if __name__ == "__main__":
    main()
