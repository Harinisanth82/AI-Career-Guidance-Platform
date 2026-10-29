@echo off
title AI Career Guidance Framework - Analytics and Research Suite
cd /d "%~dp0"
echo ===================================================================
echo AI Career Guidance Framework - Academic Analytics and Dataset Suite
echo ===================================================================
echo.

echo 1. Generating / Verifying Synthetic Historical Benchmark Dataset (300 records)...
.\backend\venv\Scripts\python.exe backend\data\generate_mock_database.py
echo.

echo 2. Running Employability Statistical Correlation and Placement Audit...
.\backend\venv\Scripts\python.exe backend\analytics\employability_statistical_analysis.py
echo.

echo 3. Running Cohort Skill-Gap and Market Deficit Analysis...
.\backend\venv\Scripts\python.exe backend\analytics\skill_gap_cohort_analysis.py
echo.

echo 4. Generating Formal Academic Research and Viva Evaluation Report...
.\backend\venv\Scripts\python.exe backend\analytics\academic_research_evaluator.py
echo.

echo ===================================================================
echo Analysis complete!
echo Generated Reports:
echo - Dataset JSON: backend\data\synthetic_students_dataset.json
echo - Dataset CSV : backend\data\synthetic_students_dataset.csv
echo - Market JSON : backend\data\career_market_benchmarks.json
echo - Thesis Doc  : backend\analytics\academic_research_report.md
echo ===================================================================
pause
