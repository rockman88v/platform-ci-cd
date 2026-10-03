# Reusable CI/CD Platform

This repository centralizes reusable GitHub Actions workflows and composite actions for .NET services on AWS ECR/EKS with GitOps and Argo CD. It intentionally does **not** provide an application-pipeline workflow: every application repository keeps thin, explicit wrappers for CI, build, deploy, verify, and promotion.

## Repositories in this workspace

- `platform-ci-cd/`: reusable workflows, shared actions, scripts, docs, and a GitOps reference example.
- `payment-service/`: independently usable .NET 8 reference application and seven workflow wrappers.

Replace every `YOUR_ORG`, `YOUR_AWS_ACCOUNT_ID`, `YOUR_AWS_REGION`, ECR, GitOps, Argo CD, and `.invalid` URL placeholder before enabling the workflows. No real secrets or account identifiers are included.

## Flow

`PR -> CI -> merge to main -> Build once -> GitOps DEV -> verify DEV -> GitOps STAGING -> verify STAGING -> GitHub production approval -> GitOps PRODUCTION -> Argo CD`.

Build publishes a full-commit-SHA tag and resolves its ECR digest. `image-metadata.json` is uploaded to the successful Build run. DEV deploy stores the original source SHA and exact Build run ID in `release-context`; later runs download both artifacts by run ID. Each application wrapper explicitly dispatches its successor after success. Promotion never accepts an arbitrary image tag and never rebuilds.

## Documentation

Start with [architecture](docs/architecture.md), [workflow contracts](docs/reusable-workflows.md), [shared actions](docs/shared-actions.md), [security setup](docs/security.md), and [onboarding](docs/onboarding.md). Each reusable workflow and composite action also has its own README under `docs/workflows/` or `docs/actions/`.

## Validation

From the workspace root, validate the reference app with `dotnet restore`, `dotnet build`, `dotnet test`, and `docker build -t payment-service:local ./payment-service`. Validate the sample Helm chart with `helm lint ./platform-ci-cd/examples/gitops-apps/apps/payment-service/base` and `helm template payment-service ...`. GitHub-hosted workflow execution, AWS OIDC/ECR, GitOps pushes, Argo CD, EKS, and Environment approvals require organization infrastructure and cannot be validated offline.

## Versioning

Application wrappers use `YOUR_ORG/platform-ci-cd/...@v1`. Publish a protected major tag only after review. For production, pin third-party actions to verified full commit SHAs and automate updates with Dependabot.