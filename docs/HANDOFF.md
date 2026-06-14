# InBody Manager — Claude Code 인계 문서

## 프로젝트 개요

체성분(인바디) 측정 데이터를 관리하는 **단일 HTML 파일 웹앱**

* 파일: `inbody-manager.html` (약 104KB)
* 의존성: Chart.js 4.4.1 (CDN), Tesseract.js 5 (CDN)
* 저장소: 없음 (단일 파일, localStorage 사용)
* 배포: 파일을 직접 열거나 정적 호스팅

\---

## 기술 스택

|항목|내용|
|-|-|
|언어|HTML/CSS/JS (단일 파일)|
|차트|Chart.js 4.4.1|
|OCR|Tesseract.js 5 (kor+eng)|
|데이터 저장|localStorage (`inbody\_records`, `inbody\_settings`)|
|JS 문법|**ES5 호환** (구형 Android WebView 대응)|

### ⚠️ JS 문법 제약사항 (중요)

구형 Android WebView 호환을 위해 아래 문법을 **절대 사용 금지**:

```
❌ const / let              → var 사용
❌ {...obj} 객체 스프레드   → Object.assign({}, obj) 사용
❌ \[...arr] 배열 스프레드   → arr.slice() / \[].concat() 사용
❌ obj?.prop 옵셔널 체이닝  → obj ? obj.prop : null 사용
❌ a ?? b 널 병합           → a != null ? a : b 사용
❌ for...of                 → for (var i=0; i<arr.length; i++) 사용
❌ 구조분해 할당             → 개별 변수 할당 사용
❌ 함수 기본 파라미터        → 함수 내부에서 처리
```

Chart.js 옵션 객체는 `makeChartOpts(base, extraScales, yMin)` 헬퍼 사용.

\---

## 파일 구조

```
inbody-manager.html
├── <head>
│   ├── CSS (인라인 \~400줄)
│   │   ├── CSS 변수 (:root) - 색상/간격
│   │   ├── Nav / Page / Card 레이아웃
│   │   ├── 통계카드 / 구성비바 / 차트박스
│   │   ├── 폼 / 테이블 / 토글 / 토스트
│   │   ├── 스캔(OCR) UI
│   │   ├── 수정 모달
│   │   ├── 목표 달성률 카드
│   │   └── 인사이트 카드
│   └── PWA 메타태그
│
├── <body>
│   ├── <nav> - 상단 네비게이션
│   ├── .mobile-nav - 모바일 하단 탭
│   │
│   ├── #page-dashboard - 대시보드
│   │   ├── 통계카드 그리드 (#statGrid)
│   │   ├── 체성분 구성비 바 (#compBar)
│   │   ├── BMI 게이지
│   │   ├── 목표 달성률 (#goalSection)
│   │   ├── 인사이트 (#insightSection)
│   │   └── 미니 차트 2개
│   │
│   ├── #page-record - 측정 입력
│   │   ├── OCR 스캔 카드 (이미지 업로드)
│   │   └── 측정값 입력 폼 (r-date, r-weight, ...)
│   │
│   ├── #page-history - 기록 목록 테이블
│   ├── #page-charts - 상세 그래프 5종
│   ├── #page-settings - 설정 + 데이터 관리 + PWA 설치
│   ├── #page-changelog - 변경 이력
│   │
│   ├── #editModalBg - 기록 수정 모달
│   ├── #toast - 알림 토스트
│   └── <script> - JS 전체 (\~63KB)
```

\---

## 주요 함수 목록 (72개)

### 데이터 레이어

|함수|설명|
|-|-|
|`loadRecords()`|localStorage에서 기록 배열 로드|
|`saveRecords(arr)`|날짜순 정렬 후 저장|
|`loadSettings()`|설정 객체 로드 (기본값 포함)|
|`saveSettingsData(s)`|설정 저장|

### 네비게이션

|함수|설명|
|-|-|
|`showPage(id)`|페이지 전환 (dashboard/record/history/charts/settings/changelog)|
|`openModal()`|`showPage('record')` 로 리다이렉트 (모달 제거됨)|
|`toggleMobileMenu()`|모바일 메뉴 토글|

### 대시보드 렌더링

|함수|설명|
|-|-|
|`renderDashboard()`|전체 대시보드 렌더링|
|`renderMiniCharts()`|체중/체지방 미니 차트|
|`renderGoals(latest, s)`|목표 달성률 카드|
|`renderInsights(records, s)`|변화 분석 인사이트|
|`setDashRange(n, btn)`|대시보드 날짜 범위 변경|

### 기록 관리

|함수|설명|
|-|-|
|`saveRecord()`|입력 탭 폼 저장|
|`buildRecord(prefix)`|폼 데이터로 레코드 객체 생성 (prefix: 'r')|
|`renderHistory()`|기록 목록 테이블 렌더링|
|`deleteRecord(id)`|ID로 기록 삭제|
|`openEditModal(id)`|수정 모달 열기|
|`saveEditRecord()`|수정 저장|
|`deleteFromEdit()`|수정 모달에서 삭제|

### 그래프

|함수|설명|
|-|-|
|`renderCharts(range)`|상세 그래프 5종 렌더링|
|`makeChartOpts(base, extraScales, yMin)`|Chart.js 옵션 생성 헬퍼|
|`showEmpty(canvasId, msg)`|빈 차트 안내 오버레이|
|`setChartsRange(n, btn)`|그래프 날짜 범위 변경|

### OCR / 이미지 스캔

|함수|설명|
|-|-|
|`processImageFile(file)`|이미지 파일 → OCR 실행|
|`runOCR(dataUrl)`|Tesseract.js OCR 실행|
|`parseInbodyText(text)`|OCR 텍스트 파싱 → 수치 추출|
|`deriveValues(d, settings)`|인식값으로 미인식 항목 환산 계산|
|`showScanResult(data, rawText)`|OCR 결과 표시|
|`applyScanResult(silent)`|결과를 폼에 적용|
|`setScanState(state, opts)`|스캔 UI 상태 전환 (idle/loading/error/success)|
|`retryOCR()`|같은 이미지로 재시도|
|`resetScan()`|스캔 초기화|

### 설정 / 데이터

|함수|설명|
|-|-|
|`loadSettingsUI()`|설정 페이지 UI 로드|
|`saveSettings()`|설정 페이지 저장|
|`exportData()`|JSON 내보내기|
|`importData(event)`|JSON 가져오기 (병합)|
|`exportCSV()`|CSV 내보내기|
|`clearAllData()`|전체 데이터 삭제|

### PWA

|함수|설명|
|-|-|
|`initPWA()`|Service Worker 등록 + 설치 배너|
|`installPWA()`|설치 프롬프트 실행|
|`triggerInstall()`|설정 페이지 설치 버튼|

### 유틸

|함수|설명|
|-|-|
|`todayStr()`|YYYY-MM-DD 형식 오늘 날짜|
|`formatDate(d)`|YYYY.MM.DD 형식 변환|
|`calcBMI(weight, heightCm)`|BMI 계산|
|`bmiStatus(bmi)`|BMI 판정 (저체중/정상/과체중/비만/고도비만)|
|`toast(msg)`|토스트 알림 표시|
|`deltaHTML(val, prev, reverse)`|변화량 HTML 생성|
|`daysDiff(dateStr)`|오늘로부터 일수 차이|
|`avgField(arr, key)`|배열 특정 필드 평균|
|`calcStreak(records)`|연속 측정 일수 계산|
|`round1(v)`|소수점 1자리 반올림|
|`getFieldVal(id)`|getElementById + .value 안전하게|

\---

## 데이터 구조

### Record 객체

```javascript
{
  id:          Number,   // Date.now() 기반 고유 ID
  date:        String,   // 'YYYY-MM-DD'
  weight:      Number,   // 체중 kg
  fatPct:      Number,   // 체지방률 %
  fatKg:       Number,   // 체지방량 kg
  muscle:      Number,   // 근육량 kg
  skeletal:    Number,   // 골격근량 kg
  water:       Number,   // 체수분 L
  bmr:         Number,   // 기초대사량 kcal
  waist:       Number,   // 허리둘레 cm
  visceral:    Number,   // 내장지방 레벨
  score:       Number,   // 바디 점수
  bmi:         Number,   // BMI
  note:        String,   // 메모
}
```

### Settings 객체

```javascript
{
  name:         String,  // 이름
  gender:       String,  // 'M' | 'F' | ''
  birth:        String,  // 'YYYY-MM-DD'
  height:       Number,  // 신장 cm
  targetWeight: Number,  // 목표 체중 kg
  targetFat:    Number,  // 목표 체지방률 %
  showTarget:   Boolean, // 목표 라인 표시
  autoBMI:      Boolean, // BMI 자동 계산
  showDelta:    Boolean, // 변화량 표시
}
```

\---

## 버전 이력

|버전|주요 내용|
|-|-|
|v1.0|최초 릴리즈 (대시보드, 입력, 기록, 그래프, 설정, 데이터 내보내기/가져오기)|
|v1.1|Tesseract.js OCR 이미지 자동 인식 (무료, 로컬 처리)|
|v1.2|입력 화면 통합 (모달 제거 → 단일 페이지)|
|v1.3|OCR 실패 시 재시도/다른이미지/초기화 버튼 추가|
|v1.4|OCR 인식값으로 미인식 항목 자동 환산 (Mifflin, Janssen 등)|
|v1.5|BMI 역산으로 앱 실제 키 추정, 환산 정확도 개선|
|v1.6|기록 수정, 목표 달성률, 변화 인사이트, PWA 지원|
|v1.7|그래프 null 데이터 처리 (NaN 갭, 빈 차트 안내)|
|v1.8|구형 Android WebView 호환 (옵셔널체이닝/스프레드/const 제거)|

\---

## 남은 개선 과제

* \[ ] localStorage 외 IndexedDB 백업 (데이터 안전성)
* \[ ] OCR 정확도 향상 (이미지 전처리 - 이진화/대비 강화)
* \[ ] 다중 사용자 프로필 전환
* \[ ] 측정 리마인더 알림 (Notification API)
* \[ ] 체성분 표준 범위 색상 표시 (연령/성별 기준)
* \[ ] 기간 비교 (이번 달 vs 지난 달)

\---

## Claude Code 작업 시작 방법

```bash
# 파일 확인
ls -lh inbody-manager.html

# 수정 후 문법 검사 (Node.js)
node --check inbody-manager.html  # HTML 내 <script> 추출 후 확인

# 또는 JS만 추출해서 검사
python3 -c "
import re
with open('inbody-manager.html') as f: c = f.read()
js = re.findall(r'<script\[^>]\*>(.\*?)</script>', c, re.DOTALL)\[-1]
with open('/tmp/check.js', 'w') as f: f.write(js)
"
node --check /tmp/check.js
```

### 코드 수정 시 주의사항

1. **JS 문법**: 위 제약사항 반드시 준수 (var, Object.assign, for문 등)
2. **차트 옵션**: `makeChartOpts()` 헬퍼 사용
3. **null 처리**: 차트 데이터는 `safe(arr)` 함수로 null→NaN 변환
4. **수정 후 node --check 필수 실행**

