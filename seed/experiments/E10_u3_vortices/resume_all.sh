#!/bin/bash
# Re-launch every unfinished E10 B2/B3 job after a container restart (each job resumes from its saved state:
# B3 per-point files in /tmp/claude-0/b3_points, 2D solves from checkpoints in /tmp/claude-0/ckpt).
cd "$(dirname "$0")"
if ! pgrep -f "[b]3_pipeline.py run" >/dev/null; then
  (setsid nohup python3 b3_pipeline.py run >> log_b3_run2.txt 2>&1 < /dev/null &)
fi
if ! pgrep -f "[b]2_run.py convergence|[b]3_compare2d.py" >/dev/null; then
  (setsid nohup bash -c "grep -q 'convergence done' log_b2.txt || python3 b2_run.py convergence >> log_b2.txt 2>&1; python3 b3_compare2d.py >> log_b3_compare2d.txt 2>&1" > /dev/null 2>&1 < /dev/null &)
fi
