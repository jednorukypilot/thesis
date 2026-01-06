@echo off
REM Build script for thesis - handles encoding and multiple passes correctly
echo Building thesis with proper encoding handling...
echo.

REM Clean temporary files
echo Cleaning temporary files...
if exist tmp\* del /q tmp\*
if exist *.aux del /q *.aux
if exist *.toc del /q *.toc
if exist *.out del /q *.out

echo.
echo Running LaTeX compilation...
latexmk -pdf -f thesis.tex

echo.
echo Build complete! Check thesis.pdf for the result.
pause