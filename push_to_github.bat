@echo off
echo Setting up remote and pushing to GitHub...
git remote add origin https://github.com/brothergbk/My-subliminal.git
git branch -M main
git push -u origin main
echo.
echo Done! Your repository is now published at:
echo https://github.com/brothergbk/My-subliminal
pause

