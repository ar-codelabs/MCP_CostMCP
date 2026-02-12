# AWS 비용 관리 MCP 서버 가이드

AI 에디터(VS Code, Cursor, Kiro 등)에서 AWS 비용을 분석하고 관리하는 MCP 서버 설정 가이드입니다.

## 📋 목차
- [사전 요구사항](#사전-요구사항)
- [MCP 서버 구성](#mcp-서버-구성)
- [설치 방법](#설치-방법)
- [MCP 서버 상세 정보](#mcp-서버-상세-정보)
- [사용 예시](#사용-예시)
- [IAM 권한 설정](#iam-권한-설정)
- [문제 해결](#문제-해결)

## 사전 요구사항

### 1. uvx 설치

**macOS:**
```bash
# Homebrew로 설치
brew install uv

# 설치 확인
uvx --version
```

**Linux:**
```bash
# 공식 설치 스크립트
curl -LsSf https://astral.sh/uv/install.sh | sh

# 쉘 재시작
source ~/.zshrc  # 또는 source ~/.bashrc

# 설치 확인
uvx --version
```

### 2. AWS 자격증명 설정

```bash
# AWS CLI 설치 확인
aws --version

# AWS 자격증명 구성
aws configure
```

필요한 정보:
- AWS Access Key ID
- AWS Secret Access Key
- Default region: `us-east-1` (권장)
- Default output format: `json`

## MCP 서버 구성

### 전체 MCP 설정 파일

```json
{
  "mcpServers": {
    "aws-billing-cost-management": {
      "command": "uvx",
      "args": ["awslabs.billing-cost-management-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "default",
        "AWS_REGION": "us-east-1",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    },
    "aws-cost-explorer": {
      "command": "uvx",
      "args": ["awslabs.cost-explorer-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "default",
        "AWS_REGION": "us-east-1",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    },
    "aws-knowledge": {
      "command": "uvx",
      "args": ["awslabs.aws-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    },
    "aws-pricing": {
      "command": "uvx",
      "args": ["awslabs.aws-pricing-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "default",
        "AWS_REGION": "us-east-1",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

## 설치 방법

### VS Code

```bash
# 프로젝트 루트에 설정 폴더 생성
mkdir -p .vscode

# MCP 설정 파일 생성
cat > .vscode/mcp.json << 'EOF'
{
  "mcpServers": {
    "aws-billing-cost-management": {
      "command": "uvx",
      "args": ["awslabs.billing-cost-management-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "default",
        "AWS_REGION": "us-east-1",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    },
    "aws-cost-explorer": {
      "command": "uvx",
      "args": ["awslabs.cost-explorer-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "default",
        "AWS_REGION": "us-east-1",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    },
    "aws-knowledge": {
      "command": "uvx",
      "args": ["awslabs.aws-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    },
    "aws-pricing": {
      "command": "uvx",
      "args": ["awslabs.aws-pricing-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "default",
        "AWS_REGION": "us-east-1",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
EOF

# VS Code 재시작
```

### Cursor

```bash
# 프로젝트 루트에 설정 폴더 생성
mkdir -p .cursor

# MCP 설정 파일 생성 (위와 동일한 내용)
cp .vscode/mcp.json .cursor/mcp.json

# Cursor 재시작
```

### Kiro

```bash
# 프로젝트 루트에 설정 폴더 생성
mkdir -p .kiro/settings

# MCP 설정 파일 생성 (위와 동일한 내용)
cp .vscode/mcp.json .kiro/settings/mcp.json

# Kiro 재시작
```

## MCP 서버 상세 정보

### 1. AWS Billing & Cost Management MCP Server

**역할:** 종합 비용 관리 및 최적화

**주요 API:**
- `get_cost_and_usage`: 비용 및 사용량 조회
- `get_cost_forecast`: 비용 예측
- `get_cost_optimization_recommendations`: 비용 최적화 권장사항
- `get_savings_plans_utilization`: Savings Plans 활용률
- `get_reservation_utilization`: Reserved Instances 활용률
- `get_free_tier_usage`: Free Tier 사용량 추적

**사용 예시:**
```
"이번 달 AWS 비용이 얼마나 나왔어?"
"비용 최적화 권장사항을 알려줘"
"Savings Plans 활용률을 확인해줘"
"Free Tier 사용량을 보여줘"
```

### 2. AWS Cost Explorer MCP Server

**역할:** 상세 비용 분석 및 예측

**주요 API:**
- `get_cost_and_usage`: 비용 및 사용량 조회
- `get_dimension_values`: 차원 값 조회 (서비스, 리전 등)
- `get_cost_forecast`: 비용 예측
- `get_usage_forecast`: 사용량 예측
- `get_cost_categories`: 비용 카테고리 관리
- `get_cost_and_usage_comparisons`: 기간별 비용 비교

**사용 예시:**
```
"이번 달 AWS 비용을 분석해주세요"
"EC2 비용이 급증한 원인을 찾아주세요"
"다음 달 예상 비용을 계산해주세요"
"지난 달과 이번 달 비용을 비교해줘"
"서비스별 비용 분포를 보여줘"
```

### 3. AWS Knowledge MCP Server

**역할:** AWS 공식 문서 검색 및 참조

**주요 API:**
- `search_documentation`: AWS 문서 검색
- `read_documentation`: 특정 문서 읽기
- `recommend`: 관련 문서 추천

**사용 예시:**
```
"Cost Explorer API 사용법을 알려줘"
"AWS 비용 최적화 베스트 프랙티스를 찾아줘"
"Savings Plans 문서를 검색해줘"
```

### 4. AWS Pricing MCP Server

**역할:** AWS 서비스 가격 정보 조회

**주요 API:**
- `get_pricing`: 서비스별 가격 정보
- `get_pricing_service_codes`: 사용 가능한 서비스 코드 목록
- `get_pricing_service_attributes`: 서비스별 속성 정보
- `get_pricing_attribute_values`: 속성별 가능한 값 조회

**사용 예시:**
```
"EC2 t3.medium 인스턴스 가격을 알려줘"
"RDS MySQL 가격을 비교해줘"
"S3 스토리지 비용을 계산해줘"
"Lambda 함수 실행 비용이 얼마야?"
```

## 사용 예시

### 기본 비용 조회

```
질문: "이번 달 AWS 비용이 얼마나 나왔어?"

AI 응답 예시:
- 현재까지 누적 비용: $1,234.56
- 예상 월말 비용: $1,850.00
- 전월 대비: +15%
```

### 서비스별 비용 분석

```
질문: "어떤 서비스가 가장 많은 비용을 발생시키고 있어?"

AI 응답 예시:
1. Amazon EC2: $450.23 (36%)
2. Amazon RDS: $320.15 (26%)
3. Amazon S3: $180.50 (15%)
4. AWS Lambda: $95.30 (8%)
5. 기타: $188.38 (15%)
```

### 비용 최적화

```
질문: "AWS 비용을 절감할 수 있는 방법을 찾아줘"

AI 응답 예시:
1. EC2 인스턴스 3개가 평균 CPU 사용률 15% 미만
   → t3.large에서 t3.medium으로 변경 시 월 $120 절감
   
2. EBS 볼륨 5개가 30일 이상 미사용
   → 삭제 시 월 $50 절감
   
3. RDS 인스턴스 1개가 저사용률
   → db.m5.large에서 db.t3.medium으로 변경 시 월 $200 절감

총 예상 절감액: 월 $370
```

### 비용 예측

```
질문: "다음 달 예상 비용을 계산해줘"

AI 응답 예시:
- 예상 비용: $1,950.00
- 현재 추세 기반 예측
- 주요 증가 요인:
  * EC2 인스턴스 증가 (5개 → 7개)
  * RDS 스토리지 증가 (250GB → 350GB)
```

### Free Tier 확인

```
질문: "Free Tier 사용량을 확인해줘"

AI 응답 예시:
⚠️ 주의 필요:
- Lambda: 850,000 / 1,000,000 요청 (85%)
- DynamoDB: 22GB / 25GB (88%)

✅ 여유 있음:
- S3: 2GB / 5GB (40%)
- EC2: 450시간 / 750시간 (60%)
```

### 가격 정보 조회

```
질문: "EC2 t3.medium 인스턴스 가격을 알려줘"

AI 응답 예시:
EC2 t3.medium (us-east-1):
- On-Demand: $0.0416/시간 ($30.37/월)
- 1년 Reserved: $0.0270/시간 ($19.71/월) - 35% 절감
- 3년 Reserved: $0.0166/시간 ($12.12/월) - 60% 절감
```

## IAM 권한 설정

### 필요한 IAM 권한

AWS Console → IAM → Policies → Create policy → JSON 탭에 아래 내용 붙여넣기:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AWSCostExplorerPermissions",
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage",
        "ce:GetCostForecast",
        "ce:GetDimensionValues",
        "ce:GetReservationUtilization",
        "ce:GetReservationCoverage",
        "ce:GetSavingsPlansUtilization",
        "ce:GetSavingsPlansCoverage",
        "ce:GetRightsizingRecommendation",
        "ce:GetSavingsPlansPurchaseRecommendation"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AWSBillingCostManagementPermissions",
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage",
        "ce:GetCostForecast",
        "budgets:ViewBudget",
        "cur:DescribeReportDefinitions",
        "cost-optimization-hub:ListRecommendations",
        "cost-optimization-hub:GetRecommendation",
        "compute-optimizer:GetEC2InstanceRecommendations",
        "compute-optimizer:GetEBSVolumeRecommendations",
        "compute-optimizer:GetLambdaFunctionRecommendations",
        "freetier:GetFreeTierUsage"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AWSPricingPermissions",
      "Effect": "Allow",
      "Action": [
        "pricing:DescribeServices",
        "pricing:GetProducts",
        "pricing:GetAttributeValues"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AWSKnowledgePermissions",
      "Effect": "Allow",
      "Action": [
        "iam:GetAccountSummary"
      ],
      "Resource": "*"
    }
  ]
}
```

### 정책 적용 방법

1. **정책 생성**
   - 정책 이름: `AWSCostMCPServerPolicy`
   - Create policy 클릭

2. **사용자에게 연결**
   - IAM → Users → 사용자 선택
   - Permissions → Add permissions
   - Attach policies directly
   - `AWSCostMCPServerPolicy` 검색 후 선택
   - Add permissions

### AWS CLI로 적용

```bash
# 정책 생성
aws iam create-policy \
  --policy-name AWSCostMCPServerPolicy \
  --policy-document file://iam_policy_cost_mcp.json

# 사용자에게 연결 (ARN은 위 명령어 결과에서 복사)
aws iam attach-user-policy \
  --user-name YOUR_USERNAME \
  --policy-arn arn:aws:iam::ACCOUNT_ID:policy/AWSCostMCPServerPolicy
```

## 문제 해결

### MCP 서버가 연결되지 않을 때

**1. uvx 설치 확인**
```bash
uvx --version
```

**2. AWS 자격증명 확인**
```bash
aws sts get-caller-identity
```

**3. MCP 서버 수동 테스트**
```bash
# 각 서버를 개별적으로 테스트
uvx awslabs.billing-cost-management-mcp-server@latest
uvx awslabs.cost-explorer-mcp-server@latest
uvx awslabs.aws-documentation-mcp-server@latest
uvx awslabs.aws-pricing-mcp-server@latest
```

**4. AI 에디터 재시작**
- 에디터 완전히 종료
- 터미널도 새로 열기
- 에디터 다시 시작

### 권한 오류가 발생할 때

**에러 메시지:**
```
AccessDeniedException: User is not authorized to perform: ce:GetCostAndUsage
```

**해결 방법:**
1. IAM 정책이 올바르게 적용되었는지 확인
2. 정책 전파 대기 (1-2분)
3. AWS 자격증명 새로고침
```bash
aws configure
```

### 특정 MCP 서버만 작동하지 않을 때

**aws-core 서버 에러:**
- Python 3.14 호환성 문제
- 해결: 해당 서버 비활성화 (필수 아님)

**aws-pricing 서버 에러:**
- 패키지 이름 확인: `awslabs.aws-pricing-mcp-server@latest`
- 권한 확인: `pricing:DescribeServices`

### 로그 확인

문제 해결을 위해 로그 레벨 변경:

```json
{
  "env": {
    "FASTMCP_LOG_LEVEL": "DEBUG"
  }
}
```

## 추가 리소스

- [AWS Cost Explorer 문서](https://docs.aws.amazon.com/cost-management/)
- [AWS Pricing 문서](https://docs.aws.amazon.com/pricing/)
- [AWS MCP 서버 GitHub](https://github.com/awslabs/mcp)
- [MCP 프로토콜 문서](https://modelcontextprotocol.io/)

## 지원

문제가 발생하거나 질문이 있으시면:
- [GitHub Issues](https://github.com/awslabs/mcp/issues)
- AWS Support 케이스 생성

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](./LICENSE) file.
