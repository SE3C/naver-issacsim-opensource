> 공개용 파생 사본 · 2026-10-23. 출처: `naver-issacsim/data/processed/experiments/h1/analysis/2026-10-16_H1_LIN055_FOUR_POLICY_COHORT_INTAKE.md` (`7f27a5e3ee9d`). 당시의 분석·PLANNED/HOLD 등 상태와 Run ID·SHA는 역사적 기록이다. 이 문서는 현재 채택 권고나 공식 평가기 명세가 아니다. 로컬 링크·개인 경로·제3자 인용은 공개 범위에 맞춰 정리했으며 원본은 별도 보존한다.

# H1 lin=.55 4정책 코호트 비교 수납 — HOLD 유지

## 원문·재현 입력과 검토 범위

- [보고서 원문](<../../../received/H1_LIN055_4POLICY_COHORT_ANALYSIS_20261016/H1_FOUR_POLICY_COHORT_REPORT.md>) · 출처·재현 안내〔원본 참조: `../../../incoming/other/reviewed/H1_LIN055_4POLICY_COHORT_ANALYSIS_20261016/PROVENANCE_AND_RUN.md` / 공개 사본 미포함〕 · 집계 CSV〔원본 참조: `../../../incoming/other/reviewed/H1_LIN055_4POLICY_COHORT_ANALYSIS_20261016/csv/policy_case_metrics.csv` / 공개 사본 미포함〕. 보고서·CSV·첨부 코드 등 **14파일 bytes 그대로** 보존했다. 외부 코드는 실행하지 않았다.
- Originals `data/raw/external_analysis/h1/2026-10-16_lin055_four_policy_cohort/`에 결과 ZIP(3325771 bytes, SHA `249237e94b9eea64eb099062417e6f6a443675c1c7fd30d0ea4b3450a1564374`)과 실제 입력 ZIP(SHA `eff60bee8fd66a5703110f3240626945a499476a9493f0256561d9deef6a9f21`)을 보존했다. 결과 CRC·명시된 13개 output checksum 및 입력 SHA 일치 확인.
- 기존 episode에서 **H5 mean/P05/min, H3 vy, H4 yaw**를 별도 CPU 계산해 주요 표와 대조했다. 보고서 전체 코드 재실행·전수 재분석·MP4 디코딩·새 GPU/학습/평가는 하지 않았다.

## 정책 연결

| 표기 | 실제 OFFICIAL training Run | 평가 checkpoint SHA |
|---|---|---|
| A 부모2700 | `20261009-142350-h1-actrate-0001-fresh3k` | `e54d3389e20ea913968ef8d3edbea5004368ff225fa6b94f73fcd91cf93ca7ae` |
| B 무변경4699 | `20261014-111135-h1-actrate-0001-unchanged-cont2k` | `722b35a127f7ae4209d94a9111ac5ee02071ba7f3b985dc9cdc0760bbe48f646` |
| C lin=.55/4650 | `20261015-105910-h1-actrate0001-lintrack-055-from2700-plus2k` | `e8a358a50832f6653b1e558788a5a676ab9a849d3ec6c64e3ed2430e9ff41814` |
| D lin=.65/4650 | `20261010-154926-h1-actrate0001-lintrack065-from2700-plus2k` | `ce7ad58657f3dd744e7cf2b7531f3d7d455773dfc6fb135f39d8a55aa49dea70` |

A는 auto-best2700, B는 endpoint4699, C/D는 선택·keeper4650이다. 서로 다른 학습량/선택 역할을 숨기지 않는다. ACTION 복원4650(`a8249db4…`)은 이번 4정책에 포함되지 않는다. Raw source_run_id/preset=null, imported-parent provenance=false/null은 외부 SHA mapping으로 덮어쓰지 않았다.

## 주요 결과

| 지표 | A | B | C | D |
|---|---:|---:|---:|---:|
| H5 진행 평균 / P05 / 최소(m) | 9.948 / 9.592 / 8.815 | 7.919 / 7.427 / 6.239 | 9.242 / 8.859 / 8.256 | 9.546 / 9.228 / 8.974 |
| H3 vy 오차(m/s) | .06727 | .06825 | .07139 | .05708 |
| H4 yaw 오차(rad/s) | .11832 | .09189 | .11256 | .17906 |

- **C vs B:** H5 진행 +1.322m, 384/384 대응 키 증가. 그러나 H3 vy +.00314m/s, H4 yaw +.02067rad/s로 악화한다. 회복과 비용을 함께 기록한다.
- **C vs D:** H4 yaw -.06649rad/s로 개선하지만 H3 vy +.01431m/s, H5 평균 -.30435m 및 하위 꼬리 손실. `.55`가 `.65`보다 전반적으로 낫다는 결론은 없다.
- **C vs A:** H5 평균 -.70666m. 부모 진행 장점을 온전히 유지한 것은 아니다. 정지/횡이동 body 전진 누수는 개선되므로 부모 자체도 무조건 우승으로 삼지 않는다.

**판정:** C 범용 후보 **HOLD 유지**, PROMOTE 없음. D 역시 축별 참고/HOLD이며 B의 기존 범용·전진/험지 대표 후보 REJECT는 유지한다(학습 COMPLETED/PASS와 별개). 원문 다음 행동은 이 결과 기록·승격 보류다. 직전 대화의 action=-.0003 +2K는 별도 **미선택 제안**이며, 이 보고서가 새 학습을 승인하거나 성공을 보장하지 않는다. angxy=-.08 완료 Run은 이번 비교에 없다.

## 해석 경계

각 3072행=8case×3평가seed×128env, 동일 key·평가 protocol/source/resolved config에 근거한 기술 비교다. 평가 seed는 독립 학습 seed가 아니며 동일 키가 동일 실제 난수 지형/trajectory를 입증하지 않는다. H3 body-frame ±vy 명령은 world 원점 복귀를 요구하지 않는다. world 순변위는 보조 진단이고 H5 body-forward 적분은 실제 tile 통과 거리와 다르다. 평가 reward 설정으로 학습 reward를 역추정하지 않는다. 영상·구간 시계열 미포함이므로 계단 완주나 전환 응답을 새로 확인했다고 쓰지 않는다. 공식 점수·reward 인과·새 합성점수로 환산하지 않는다.
