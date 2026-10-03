#!/usr/bin/env python3
"""Read and validate the app deploy.yaml without logging secret values."""
import json
import sys
from pathlib import Path

import yaml


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: read-deploy-config.py DEPLOY_YAML ENVIRONMENT")
    config_path = Path(sys.argv[1])
    environment = sys.argv[2]
    with config_path.open(encoding="utf-8") as stream:
        config = yaml.safe_load(stream)
    try:
        deployment = config["deployment"]
        target = deployment["environments"][environment]
        gitops = deployment["gitops"]
        tests = config.get("tests", {})
        result = {
            "application": config["application"],
            "imageRepository": config["image"]["repository"],
            "imageTagPath": config["image"].get("tagPath", "image.tag"),
            "imageDigestPath": config["image"].get("digestPath", "image.digest"),
            "gitopsRepository": gitops["repository"],
            "chartPath": gitops["chartPath"],
            "valuesFile": target["valuesFile"],
            "argoServer": target["argo"]["server"],
            "argoApplication": target["argo"]["application"],
            "baseUrl": target.get("baseUrl", ""),
            "smokeEnabled": bool(tests.get("smoke", {}).get("enabled", False)),
            "smokePath": tests.get("smoke", {}).get("path", "tests/smoke"),
            "e2eEnabled": bool(tests.get("e2e", {}).get("enabled", False)),
            "e2ePath": tests.get("e2e", {}).get("path", "tests/e2e"),
            "e2eFramework": tests.get("e2e", {}).get("framework", "shell"),
        }
    except (KeyError, TypeError) as exc:
        raise SystemExit(f"invalid deploy config or missing field: {exc}") from exc
    print(json.dumps(result))


if __name__ == "__main__":
    main()
