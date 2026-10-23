# H1 H-008 LINTRACK075 PERSONAL continuation 원본

## 범위와 provenance

- 실행: 2026-09-17~18 UTC / 개인 NVIDIA Brev L40S
- 가설: H-008 LINTRACK075의 3K final `model_2998.pt`에서 reward 변경 없이 continuation
- parent SHA-256: `d9a30c8a117f69cac49c4e640500f0fa8d88de72d6c61855f1e147ea6c1912ae`
- 요청: 추가 2,000 iterations
- 실제 console 범위: global 2998~4997
- final numbered checkpoint: `model_4997.pt`, SHA-256 `e6deed62c1dfff4d5bdaac4cf77ee7308f91f04f9ea6db32a8f80f3e5db922a2`
- 환경: PERSONAL. OFFICIAL 성능·제출 근거가 아니다.

`received/`에는 GitHub Release에서 받은 바이트를 변경하지 않고 보관한다. canonical
evidence는 main archive이며, post-run provenance archive는 generic `issacsimz run` 실행 뒤
보강한 supplementary reconstruction이다. 후자는 execution-time profile provenance를 대체하지
않는다.

## 수신 원본 manifest

| 파일 | 역할 | bytes | SHA-256 |
| --- | --- | ---: | --- |
| `20260917-234047-h1-h008-cont2k-from-2998.tar.gz` | canonical training evidence | 153,896,399 | `b669bf1b90a67a4468e6851ab237538bbab6450144b3e4f5e9eecbfeb6777d9e` |
| `20260917-234047-h1-h008-cont2k-from-2998.tar.gz.sha256` | canonical archive sidecar | 114 | `7970f48fa0d9b4ab4287224f4a6a701a5d61e680768d405bc41feb05ab0be4ab` |
| `20260917-234047-h1-h008-cont2k-from-2998.tar.gz.metadata.json` | archive packing metadata | 246 | `6e86a42826fe571492b40ddf04e703fd5fa3b9f0909e08cbac54450f550a3e92` |
| `20260917-234047-h1-h008-cont2k-from-2998-POSTRUN-PROVENANCE.tar.gz` | post-run supplementary provenance | 249,285 | `a95494a534edec9915d211c4e66ef674203ee7f0c1acee7b39952179215d9ae5` |
| `20260917-234047-h1-h008-cont2k-from-2998-POSTRUN-PROVENANCE.tar.gz.sha256` | supplementary sidecar as received | 149 | `c253d1a1508ee788a8279128280d493cd9aa3cbbc03519713c65888645fdc1c9` |

Source Release: <https://github.com/SE3C/naver-issacsim-nvidia/releases/tag/20260917-234047-h1-h008-cont2k-from-2998>

## Verification and known limitation

- outer canonical archive SHA-256 matches its received sidecar and Release digest.
- archive-internal `SHA256SUMS` verifies 41/41 listed files.
- 21 numbered checkpoints are present: `model_3000.pt` through `model_4997.pt` at 100-step intervals plus final.
- `validation.json` is `WARN`, not `PASS`: `profile`, `source_checkpoint`, and `resume_lineage` are null because the run used generic `issacsimz run` rather than the profile-aware train wrapper.
- `mode=personal`, exit code is 0, native TensorBoard is preserved, and no collection error is recorded.
- exported automatic `model_best.pt` is `model_4900.pt` (SHA-256 `b9086b1f…41d4f3c9`), while the retained final numbered checkpoint is `model_4997.pt`. The final checkpoint is the representative policy under the resume policy; do not silently substitute automatic `model_best`.

The archive is immutable evidence. Do not flatten it, delete duplicate timestamped native exports,
or replace it with the derived download handoff. Detailed interpretation belongs in
`naver-issacsim`, not this raw archive.
