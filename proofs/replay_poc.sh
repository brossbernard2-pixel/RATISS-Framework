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

# --- runs millénaires, 2026-09-13 (scellés du jour) ---
run "M1 papier OpenAI Navier-Stokes (scellé 2026-09-13)" \
  python3 -m ratiss audit --url "https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf" --sha256 0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f
run "M2 tarball Lean OpenAI au commit f9e8bc5b (scellé 2026-09-13)" \
  python3 -m ratiss audit --url "https://codeload.github.com/openai/NavierStokesAndEuler/tar.gz/f9e8bc5b38b6e212696e8a30e3e91517af887bbd" --sha256 9832374e0926a8a9dfb19699e50bf8ddb957fb9e961e7cc85b8fb689eda2b1b7
run "M3 arXiv 2410.22920v3 pdf (scellé 2026-09-13)" \
  python3 -m ratiss audit --url "https://arxiv.org/pdf/2410.22920v3" --sha256 14c3a2423cbcec2d6ca5c54258ae4bd978f66631165fdb6217248bda280d45e8
run "M3b doi 10.48550/arXiv.2410.22920" \
  python3 -m ratiss doi 10.48550/arXiv.2410.22920

echo
echo "Attendu millénaire : M1, M2, M3, M3b = exit 0 (scellés du 2026-09-13)."
