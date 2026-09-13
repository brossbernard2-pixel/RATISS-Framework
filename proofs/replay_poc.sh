#!/usr/bin/env bash
# Rejeu R7 de la preuve de concept du 2026-09-13.
# Attendu : 9 exits 0 (conformes) + 1 exit 1 (contrôle négatif N1).
set -u
cd "$(dirname "$0")/.." || exit 2

run() {
  desc="$1"; shift
  "$@" >/dev/null 2>&1
  code=$?
  printf '%-58s exit %s\n' "$desc" "$code"
  return 0
}

run "Z1 zenodo 6164620 README.md" \
  python3 -m ratiss audit-zenodo --record 6164620 --file README.md
run "Z2 zenodo 7347926 yolov5-v7.0.zip" \
  python3 -m ratiss audit-zenodo --record 7347926 --file "ultralytics/yolov5-v7.0.zip"
run "Z3 zenodo 884117 Data_for_Policy_2017_paper_43.pdf" \
  python3 -m ratiss audit-zenodo --record 884117 --file Data_for_Policy_2017_paper_43.pdf
run "Z4 zenodo 1427076 article.pdf (1856)" \
  python3 -m ratiss audit-zenodo --record 1427076 --file article.pdf
run "P1 pypi openai-3.13.0 wheel" \
  python3 -m ratiss audit --url "https://files.pythonhosted.org/packages/63/7f/ee9ebb7c5ab7abf016969faec7c748a91c1fd893078bfe1e5ba5d82e96c2/openai-3.13.0-py3-none-any.whl" --sha256 e35b1f6fe99245e86e37504d9fad1ad2a363807307c424232c1d849bd0666c8e
run "P2 pypi requests-2.34.2 wheel" \
  python3 -m ratiss audit --url "https://files.pythonhosted.org/packages/a0/f4/c67b0b3f1b9245e8d266f0f112c500d50e5b4e83cb6f3b71b6528104182a/requests-2.34.2-py3-none-any.whl" --sha256 2a0d60c172f83ac6ab31e4554906c0f3b3588d37b5cb939b1c061f4907e278e0
run "D1 doi 10.31235/osf.io/8jwhk" \
  python3 -m ratiss doi 10.31235/osf.io/8jwhk
run "D2 doi 10.1207/s15327906mbr0404_6" \
  python3 -m ratiss doi 10.1207/s15327906mbr0404_6
run "D3 doi 10.1201/9781003267218-8" \
  python3 -m ratiss doi 10.1201/9781003267218-8
run "N1 CONTROLE NEGATIF (divergence attendue, exit 1)" \
  python3 -m ratiss audit --url "https://files.pythonhosted.org/packages/a0/f4/c67b0b3f1b9245e8d266f0f112c500d50e5b4e83cb6f3b71b6528104182a/requests-2.34.2-py3-none-any.whl" --sha256 e35b1f6fe99245e86e37504d9fad1ad2a363807307c424232c1d849bd0666c8e

echo
echo "Attendu : Z1-Z4, P1-P2, D1-D3 = exit 0 ; N1 = exit 1."
