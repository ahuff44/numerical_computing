
@echo off
FOR %%P IN (1, 2, 3, 4, 6, 8, 12, 24, 48) DO (
    python stopwatch.py --start
    mpirun -n %%P python.exe speed.py
    echo %%P processes:
    python stopwatch.py --stop
    echo -------------
)
