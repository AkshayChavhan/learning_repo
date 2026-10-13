#!/usr/bin/env bash
# Build the image and push it to Amazon ECR - the lecture's three commands, with checks.
#
#   ./push-to-ecr.sh              build, login, tag, push
#   ./push-to-ecr.sh --dry-run    only print the commands it would run
#   ./push-to-ecr.sh --create     also create the ECR repository if it doesn't exist
#
# Reads AWS_ACCOUNT_ID, AWS_REGION, ECR_REPO, IMAGE_TAG from ./.env (see .env.example).
set -euo pipefail

cd "$(dirname "$0")"
[ -f .env ] && set -a && . ./.env && set +a

AWS_REGION="${AWS_REGION:-ap-south-1}"
ECR_REPO="${ECR_REPO:-backend}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
DRY_RUN=false; CREATE=false
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --create)  CREATE=true ;;
    *) echo "unknown option: $arg"; exit 2 ;;
  esac
done

# ---- checks ------------------------------------------------------------------
if [ -z "${AWS_ACCOUNT_ID:-}" ]; then
  echo "AWS_ACCOUNT_ID is not set. Copy .env.example to .env and fill it in." >&2; exit 1
fi
if ! $DRY_RUN; then
  command -v aws >/dev/null  || { echo "aws CLI not found.  brew install awscli  then  aws configure   (note 244)" >&2; exit 1; }
  docker info >/dev/null 2>&1 || { echo "Docker daemon is not running. Open Docker Desktop." >&2; exit 1; }
  aws sts get-caller-identity >/dev/null 2>&1 || { echo "AWS CLI has no working credentials. Run: aws configure" >&2; exit 1; }
fi

REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"   # registry host for your region
URI="${REGISTRY}/${ECR_REPO}"                                       # repository URI = the image name

run() {                      # print every command before running it, so the output doubles as a lesson
  echo
  echo "\$ $*"
  $DRY_RUN || eval "$@"
}

echo "registry : $REGISTRY"
echo "image    : $URI:$IMAGE_TAG"
$DRY_RUN && echo "(dry run - nothing is executed)"

# ---- 0. (optional) create the repository, same as the console's Create repository ----
if $CREATE; then
  run "aws ecr describe-repositories --repository-names $ECR_REPO --region $AWS_REGION >/dev/null 2>&1 \
    || aws ecr create-repository --repository-name $ECR_REPO --region $AWS_REGION --query 'repository.repositoryUri' --output text"
fi

# ---- 1. build locally ---------------------------------------------------------
run "docker build -t $ECR_REPO:$IMAGE_TAG ."

# ---- 2. log Docker in to ECR with a temporary (12h) password from the AWS CLI ---
run "aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $REGISTRY"

# ---- 3. tag with the ECR name (adds a name, copies nothing) ---------------------
run "docker tag $ECR_REPO:$IMAGE_TAG $URI:$IMAGE_TAG"

# ---- 4. push ------------------------------------------------------------------
run "docker push $URI:$IMAGE_TAG"

$DRY_RUN || { echo; echo "Pushed. Verify:"; echo "  aws ecr describe-images --repository-name $ECR_REPO --region $AWS_REGION"; }
