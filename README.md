# AWS MCP 대시보드 프로젝트

VS Code에서 사용할 수 있는 AWS 비용 관리 및 DevOps 모니터링 대시보드입니다.

## 🚀 빠른 시작

### 1단계: 설정

```bash
# 실행 권한 부여 및 자동 설정
chmod +x setup.sh
./setup.sh
```

이 스크립트가 자동으로:
- ✅ Python 가상환경 생성
- ✅ 필요한 패키지 설치 (boto3, streamlit, plotly 등)

### 2단계: AWS 자격증명 설정

```bash
aws configure
```

입력 정보:
- AWS Access Key ID
- AWS Secret Access Key  
- Default region (예: us-east-1)
- Default output format (json)

### 3단계: 대시보드 실행

```bash
# 비용 관리 대시보드
./run_cost_dashboard.sh

# DevOps 대시보드 (다른 터미널에서)
./run_devops_dashboard.sh
```

## 📁 프로젝트 구조

```
.
├── cost_mcp_readme.md              # 비용 관리 MCP 가이드
├── devops_mcp_readme.md            # DevOps MCP 가이드
├── mcp_cost_config.json            # 비용 관리 MCP 설정 (5개 서버)
├── mcp_devops_config.json          # DevOps MCP 설정 (12개 서버)
├── cost_dashboard_streamlit.py     # 비용 대시보드
├── devops_dashboard_streamlit.py   # DevOps 대시보드
├── requirements.txt                # Python 패키지
├── setup.sh                        # 자동 설정 스크립트
├── run_cost_dashboard.sh           # 비용 대시보드 실행
└── run_devops_dashboard.sh         # DevOps 대시보드 실행
```

## 📊 대시보드 기능

### 💰 비용 관리 대시보드 (포트 8501)

- **실시간 비용 모니터링**
  - 이번 달 누적 비용
  - 월말 예상 비용
  - 예상 절감 가능액

- **서비스별 비용 분석**
  - 파이 차트 시각화
  - 상위 10개 서비스

- **일별 비용 추세**
  - 최근 30일 그래프
  - 평균/최대/최소 통계

- **비용 최적화 권장사항**
  - EC2 인스턴스 크기 조정
  - 미사용 EBS 볼륨 삭제
  - RDS 인스턴스 최적화

- **Free Tier 사용량 추적**
  - Lambda, DynamoDB, S3, EC2
  - 사용률 프로그레스 바
  - 한도 근접 경고

### 🚀 DevOps 대시보드 (포트 8502)

- **인프라 요약**
  - EC2 인스턴스 현황
  - ECS 클러스터 및 서비스
  - Lambda 함수 개수
  - CloudWatch 알람 상태

- **활성 알람 모니터링**
  - 알람 상태 분포 차트
  - 알람 상세 정보

- **EC2 인스턴스 관리**
  - CPU 사용률 모니터링
  - 인스턴스 상태 확인
  - 시각화된 메트릭

- **Lambda 함수 통계**
  - 호출 횟수 (24시간)
  - 에러 발생 현황
  - 함수별 비교 차트

- **로그 분석**
  - CloudWatch Logs 최근 이벤트
  - 로그 그룹별 조회

- **활동 추적**
  - CloudTrail 이벤트
  - 사용자별 활동 내역
  - 이벤트 타입별 통계

## 🔧 설정

### AWS 리전 변경
대시보드 사이드바에서 리전 선택 가능:
- us-east-1 (버지니아 북부)
- us-west-2 (오레곤)
- ap-northeast-2 (서울)
- eu-west-1 (아일랜드)

### 자동 새로고침
DevOps 대시보드에서 "자동 새로고침" 옵션 활성화 시 1분마다 업데이트


## 🛠️ 문제 해결

### Python이 없다고 나올 때

```bash
# Homebrew로 설치
brew install python@3.11
```

### AWS 자격증명 오류

```bash
# 자격증명 확인
aws sts get-caller-identity

# 자격증명 재설정
aws configure
```

### 포트가 이미 사용 중일 때

```bash
# 다른 포트로 실행
streamlit run cost_dashboard_streamlit.py --server.port 8503
```

### 가상환경 수동 활성화

```bash
source venv/bin/activate
```

### 패키지 재설치

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## 📝 필요한 IAM 권한

### 비용 관리 대시보드
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage",
        "ce:GetCostForecast",
        "compute-optimizer:GetEC2InstanceRecommendations",
        "pricing:GetProducts"
      ],
      "Resource": "*"
    }
  ]
}
```

### DevOps 대시보드
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:DescribeAlarms",
        "cloudwatch:GetMetricStatistics",
        "ec2:DescribeInstances",
        "ecs:ListClusters",
        "ecs:ListServices",
        "lambda:ListFunctions",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams",
        "logs:GetLogEvents",
        "cloudtrail:LookupEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

## 🎯 다음 단계

### 1. MCP 서버 설정

프로젝트에 포함된 MCP 설정 파일을 사용하세요:

- `mcp_cost_config.json` - 비용 관리용 (5개 MCP 서버)
- `mcp_devops_config.json` - DevOps용 (12개 MCP 서버)

**주요 MCP 서버:**

**비용 관리:**
- `aws-core` ⭐ - MCP 서버 조율 및 세션 관리 (필수)
- `aws-billing-cost-management` - 비용 분석 및 최적화
- `aws-cost-explorer` ⭐ - 상세 비용 분석 및 예측
- `aws-knowledge` - AWS 문서 접근
- `aws-pricing` - 가격 정보

**DevOps:**
- `aws-core` ⭐ - MCP 서버 조율 및 세션 관리 (필수)
- `aws-ccapi` ⭐ - Cloud Control API를 통한 리소스 관리
- `aws-cloudwatch` - 모니터링 및 알람
- `aws-iac` - 인프라 코드 (CloudFormation/CDK)
- `aws-iam` - 권한 관리
- `aws-cloudtrail` - 활동 추적
- `aws-prometheus` - Prometheus 메트릭
- `aws-eks/ecs` - 컨테이너 관리
- `aws-serverless/lambda` - 서버리스 관리

**VS Code에서 사용하기:**
```bash
# 비용 관리 설정 복사
cp mcp_cost_config.json .vscode/mcp.json

# 또는 DevOps 설정 복사
cp mcp_devops_config.json .vscode/mcp.json

# VS Code 재시작
```

자세한 내용은 `cost_mcp_readme.md` 및 `devops_mcp_readme.md` 참조

### 2. 대시보드 커스터마이징

Python 파일을 수정하여 필요에 맞게 커스터마이징하세요

## 💡 유용한 명령어

```bash
# 가상환경 비활성화
deactivate

# 데이터 새로고침
# 대시보드 사이드바에서 "데이터 새로고침" 버튼 클릭

# 두 대시보드 동시 실행
./run_cost_dashboard.sh &
./run_devops_dashboard.sh
```

## 📚 추가 리소스

- [AWS Cost Explorer 문서](https://docs.aws.amazon.com/cost-management/)
- [AWS CloudWatch 문서](https://docs.aws.amazon.com/cloudwatch/)
- [Streamlit 문서](https://docs.streamlit.io/)
- [Boto3 문서](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## 🤝 기여

이슈나 개선 사항이 있으시면 GitHub Issues를 통해 알려주세요!

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](./LICENSE) file.
