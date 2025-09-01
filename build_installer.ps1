# Step 1: Clean up old build artifacts
Write-Host "Cleaning up old build directories (dist, build)..."
if (Test-Path -Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path -Path "build") { Remove-Item -Recurse -Force "build" }

# Step 2: Run PyInstaller to build the application
Write-Host "Running PyInstaller to build the application..."
python -m PyInstaller build.spec

# Check if PyInstaller succeeded by looking for the dist directory
if (Test-Path -Path "dist") {
    Write-Host "PyInstaller build completed successfully."
    
    # Step 2: Find the latest build directory created by PyInstaller
    $buildDir = Get-ChildItem -Path "dist" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

    if ($buildDir) {
        # Construct the full path to the build directory
        $fullPath = $buildDir.FullName
        
        # Step 3: Run the NSIS compiler to create the installer
        Write-Host "Running NSIS to create the installer..."
        & "C:\Program Files (x86)\NSIS\makensis.exe" /D"BUILD_DIR=$fullPath" installer.nsi
        Write-Host "Installer created successfully."
    } else {
        Write-Host "Error: Build directory was not found in 'dist' after PyInstaller run."
    }
} else {
    Write-Host "Error: PyInstaller failed to create a 'dist' directory. Build aborted."
}