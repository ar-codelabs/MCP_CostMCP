# MCP_CostMCP
AWS Billing and Cost Management MCP 서버

# AWS 비용 관리 MCP 서버 가이드

VS Code에서 AI 에이전트를 활용한 AWS 비용 분석 및 최적화 가이드입니다.

## 📋 목차
- [개요](#개요)
- [사전 요구사항](#사전-요구사항)
- [설치 방법](#설치-방법)
- [MCP 서버 구성](#mcp-서버-구성)
- [주요 기능](#주요-기능)
- [사용 예시](#사용-예시)
- [비용 정보](#비용-정보)
- [문제 해결](#문제-해결)

## 개요

AWS Billing and Cost Management MCP 서버를 사용하면 AI 에이전트를 통해 다음과 같은 작업을 수행할 수 있습니다:

- 💰 실시간 AWS 비용 분석
- 📊 서비스별 비용 분석 및 추세 파악
- 💡 비용 최적화 권장사항 제공
- 🎯 예산 관리 및 알림 설정
- 📈 Savings Plans 및 Reserved Instances 분석
- 🆓 AWS Free Tier 사용량 추적
- 🗄️ S3 Storage Lens 분석

## 사전 요구사항

### 1. Python 및 uv 설치

**macOS/Linux:**
```bash
# uv 설치
curl -LsSf https://astral.sh/uv/install.sh | sh

# Python 3.10 이상 설치
uv python install 3.10
```

**Windows:**
```powershell
# PowerShell에서 실행
irm https://astral.sh/uv/install.ps1 | iex

# Python 3.10 이상 설치
uv python install 3.10
```

### 2. AWS 자격증명 설정

AWS CLI가 설치되어 있고 자격증명이 구성되어 있어야 합니다.

```bash
# AWS CLI 설치 확인
aws --version

# AWS 자격증명 구성
aws configure
```

필요한 정보:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (예: us-east-1)
- Default output format (json 권장)

### 3. IAM 권한 설정

다음 권한이 필요합니다:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage",
        "ce:GetCostForecast",
        "ce:GetReservationUtilization",
        "ce:GetSavingsPlansUtilization",
        "cost-optimization-hub:ListRecommendations",
        "compute-optimizer:GetEC2InstanceRecommendations",
        "compute-optimizer:GetEBSVolumeRecommendations",
        "budgets:ViewBudget",
        "pricing:GetProducts",
        "freetier:GetFreeTierUsage",
        "s3:GetStorageLensConfiguration",
        "s3:ListStorageLensConfigurations"
      ],
      "Resource": "*"
    }
  ]
}
```

## 설치 방법

### VS Code에서 MCP 설정

1. **VS Code 설정 파일 열기**

프로젝트 루트에 `.vscode` 폴더를 생성하고 `mcp.json` 파일을 만듭니다:

```bash
mkdir -p .vscode
touch .vscode/mcp.json
```

2. **MCP 구성 파일 작성**

`.vscode/mcp.json` 파일에 다음 내용을 추가합니다:

**macOS/Linux:**
```json
{
  "mcpServers": {
    "aws-billing-cost-management": {
      "command": "uvx",
      "args": [
        "awslabs.billing-cost-management-mcp-server@latest"
      ],
      "env": {
        "AWS_PROFILE": "default",
        "AWS_REGION": "us-east-1",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "aws-billing-cost-management": {
      "command": "uvx",
      "args": [
        "awslabs.billing-cost-management-mcp-server@latest"
      ],
      "env": {
        "AWS_PROFILE": "default",
        "AWS_REGION": "us-east-1",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

3. **VS Code 재시작**

설정을 적용하기 위해 VS Code를 재시작합니다.

## MCP 서버 구성

### 환경 변수 설명

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `AWS_PROFILE` | 사용할 AWS 프로필 이름 | `default` |
| `AWS_REGION` | AWS 리전 | `us-east-1` |
| `FASTMCP_LOG_LEVEL` | 로그 레벨 (ERROR, INFO, DEBUG) | `ERROR` |

### S3 Storage Lens 설정 (선택사항)

S3 Storage Lens 기능을 사용하려면 추가 환경 변수가 필요합니다:

```json
{
  "mcpServers": {
    "aws-billing-cost-management": {
      "command": "uvx",
      "args": [
        "awslabs.billing-cost-management-mcp-server@latest"
      ],
      "env": {
        "AWS_PROFILE": "default",
        "AWS_REGION": "us-east-1",
        "FASTMCP_LOG_LEVEL": "ERROR",
        "STORAGE_LENS_CONFIG_ID": "your-storage-lens-config-id",
        "STORAGE_LENS_ATHENA_DATABASE": "your-athena-database",
        "STORAGE_LENS_ATHENA_TABLE": "your-athena-table",
        "STORAGE_LENS_ATHENA_OUTPUT_LOCATION": "s3://your-bucket/query-results/"
      }
    }
  }
}
```

## 주요 기능

### 1. 비용 분석

- **현재 월 비용 조회**: 이번 달 누적 비용 확인
- **서비스별 비용 분석**: 각 AWS 서비스별 비용 분석
- **일별/월별 비용 추세**: 시간에 따른 비용 변화 추적
- **비용 예측**: 월말 예상 비용 계산

### 2. 비용 최적화

- **EC2 인스턴스 최적화**: 사용률 기반 인스턴스 크기 조정 권장
- **EBS 볼륨 최적화**: 미사용 볼륨 식별 및 삭제 권장
- **RDS 최적화**: 데이터베이스 인스턴스 크기 조정
- **Lambda 최적화**: 메모리 및 실행 시간 최적화

### 3. 예산 관리

- **예산 생성 및 관리**: 월별/분기별 예산 설정
- **예산 알림**: 임계값 초과 시 알림
- **예산 대비 실제 비용**: 예산 사용률 추적

### 4. Savings Plans & Reserved Instances

- **활용률 분석**: 현재 Savings Plans 활용률
- **권장사항**: 추가 구매 권장사항
- **비용 절감 계산**: 예상 절감액 계산

### 5. Free Tier 추적

- **Free Tier 사용량**: 현재 Free Tier 사용 현황
- **초과 예상**: Free Tier 초과 예상 서비스
- **알림**: Free Tier 한도 근접 알림

## 사용 예시

VS Code에서 AI 에이전트(예: GitHub Copilot Chat, Continue 등)와 함께 다음과 같이 사용할 수 있습니다:

### 예시 1: 이번 달 비용 조회

```
프롬프트: "이번 달 AWS 비용이 얼마나 나왔는지 알려줘"

응답 예시:
- 현재까지 누적 비용: $1,234.56
- 예상 월말 비용: $1,850.00
- 전월 대비: +15%
```

### 예시 2: 서비스별 비용 분석

```
프롬프트: "어떤 AWS 서비스가 가장 많은 비용을 발생시키고 있어?"

응답 예시:
1. Amazon EC2: $450.23 (36%)
2. Amazon RDS: $320.15 (26%)
3. Amazon S3: $180.50 (15%)
4. AWS Lambda: $95.30 (8%)
5. 기타: $188.38 (15%)
```

### 예시 3: 비용 최적화 권장사항

```
프롬프트: "AWS 비용을 절감할 수 있는 방법을 찾아줘"

응답 예시:
1. EC2 인스턴스 3개가 평균 CPU 사용률 15% 미만
   → t3.large에서 t3.medium으로 변경 시 월 $120 절감
   
2. EBS 볼륨 5개가 30일 이상 미사용
   → 삭제 시 월 $50 절감
   
3. RDS 인스턴스 1개가 저사용률
   → db.m5.large에서 db.t3.medium으로 변경 시 월 $200 절감

총 예상 절감액: 월 $370
```

### 예시 4: 특정 기간 비용 분석

```
프롬프트: "지난 3개월간 비용 추세를 보여줘"

응답 예시:
- 10월: $1,450.00
- 11월: $1,680.00 (+15.9%)
- 12월: $1,850.00 (+10.1%)

주요 증가 원인:
- EC2 인스턴스 증가 (2개 → 5개)
- RDS 스토리지 증가 (100GB → 250GB)
```

### 예시 5: Free Tier 사용량 확인

```
프롬프트: "Free Tier 사용량을 확인해줘"

응답 예시:
⚠️ 주의 필요:
- Lambda: 850,000 / 1,000,000 요청 (85%)
- DynamoDB: 22GB / 25GB (88%)

✅ 여유 있음:
- S3: 2GB / 5GB (40%)
- EC2: 450시간 / 750시간 (60%)
```

### 예시 6: 예산 설정

```
프롬프트: "월 예산을 $2,000로 설정하고 80% 도달 시 알림 받고 싶어"

응답 예시:
예산이 생성되었습니다:
- 예산 이름: Monthly-Budget-2024
- 예산 금액: $2,000/월
- 알림 설정:
  * 80% ($1,600) 도달 시 이메일 알림
  * 100% ($2,000) 도달 시 이메일 알림
```

## 비용 정보

### MCP 서버 비용
- **MCP 서버 자체**: 무료 (오픈소스)
- **로컬 실행**: 추가 비용 없음

### AWS API 호출 비용

대부분의 API 호출은 무료이거나 매우 저렴합니다:

| API | 비용 | 비고 |
|-----|------|------|
| Cost Explorer | $0.01/요청 | 캐싱으로 최소화 가능 |
| Compute Optimizer | 무료 | - |
| AWS Budgets | 처음 2개 무료, 이후 $0.02/일 | - |
| Pricing API | 무료 | - |
| Free Tier API | 무료 | - |

### 예상 월 비용

**일반적인 사용 (하루 10-20회 조회):**
- Cost Explorer API: ~$2-5/월
- 기타 API: 무료
- **총 예상 비용: $2-5/월**

**집중적인 사용 (하루 50-100회 조회):**
- Cost Explorer API: ~$10-15/월
- 기타 API: 무료
- **총 예상 비용: $10-15/월**

### 비용 절감 팁

1. **캐싱 활용**: 같은 데이터를 반복 조회하지 않기
2. **조회 빈도 조절**: 실시간이 아닌 하루 1-2회 정기 조회
3. **필요한 데이터만**: 전체 기간이 아닌 필요한 기간만 조회
4. **대시보드 활용**: 자주 보는 데이터는 CloudWatch 대시보드 활용

## 문제 해결

### MCP 서버가 연결되지 않을 때

1. **uv 설치 확인**
```bash
uv --version
```

2. **Python 버전 확인**
```bash
python3 --version  # 3.10 이상이어야 함
```

3. **AWS 자격증명 확인**
```bash
aws sts get-caller-identity
```

### 권한 오류가 발생할 때

IAM 정책에 필요한 권한이 모두 포함되어 있는지 확인:

```bash
# 현재 사용자의 권한 확인
aws iam get-user-policy --user-name YOUR_USERNAME --policy-name YOUR_POLICY_NAME
```

### 로그 확인

문제 해결을 위해 로그 레벨을 변경:

```json
{
  "env": {
    "FASTMCP_LOG_LEVEL": "DEBUG"
  }
}
```

### 일반적인 오류 메시지

| 오류 | 원인 | 해결 방법 |
|------|------|----------|
| `AccessDenied` | IAM 권한 부족 | IAM 정책 확인 및 권한 추가 |
| `InvalidClientTokenId` | AWS 자격증명 오류 | `aws configure` 재실행 |
| `RegionDisabled` | 리전 미활성화 | 활성화된 리전으로 변경 |
| `ThrottlingException` | API 호출 제한 초과 | 잠시 후 재시도 |

## 추가 리소스

- [AWS Billing and Cost Management 문서](https://docs.aws.amazon.com/cost-management/)
- [AWS MCP 서버 공식 문서](https://awslabs.github.io/mcp/servers/billing-cost-management-mcp-server)
- [AWS Cost Explorer API 문서](https://docs.aws.amazon.com/cost-management/latest/APIReference/API_Operations_AWS_Cost_Explorer_Service.html)
- [AWS 비용 최적화 베스트 프랙티스](https://aws.amazon.com/pricing/cost-optimization/)

## 지원

문제가 발생하거나 질문이 있으시면:
- [GitHub Issues](https://github.com/awslabs/mcp/issues)
- AWS Support 케이스 생성

---

**마지막 업데이트**: 2024년 2월
**버전**: 1.0.0
