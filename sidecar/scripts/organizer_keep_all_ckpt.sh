#!/bin/bash
# Run-specific adaptation of the organizer's keep_all_ckpt.sh procedure.
BASE="$1"
RUN="$2"
TRAIN_PID="$3"
KEEP="$BASE/backup_log/$(basename "$RUN")"

mkdir -p "$KEEP"
echo "대상 학습: $RUN"
echo "복사 위치: $KEEP"
copy_available() {
  for f in "$RUN"/model_*.pt; do
    [ -f "$f" ] || continue
    n=$(basename "$f")
    [ -f "$KEEP/$n" ] && continue
    a=$( { wc -c < "$f"; } 2>/dev/null ) || continue
    sleep 3
    b=$( { wc -c < "$f"; } 2>/dev/null ) || continue
    [ "$a" = "$b" ] && cp "$f" "$KEEP/$n" 2>/dev/null && echo "  받음: $n"
  done
}
while kill -0 "$TRAIN_PID" 2>/dev/null; do
  copy_available
  sleep 10
done
copy_available
echo "학습이 끝났습니다 — 받은 체크포인트 $(ls "$KEEP" | wc -l | tr -d ' ')개 ($KEEP)"
