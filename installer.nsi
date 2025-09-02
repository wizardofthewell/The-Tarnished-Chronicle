; NSIS Installer Script for ER Boss Checklist

;--------------------------------
; General
;--------------------------------

!define APP_NAME "ER Boss Checklist"
!define COMPANY_NAME "TheTarnishedChronicle"
!define APP_VERSION "1.0.3"
!define EXE_NAME "ER_Boss_Checklist.exe" ; Static EXE name
!define ICON_FILE "assets\icons\app_logo.ico"
!define OUTPUT_FILENAME "ER_Boss_Checklist_Setup.exe"

;--------------------------------
; MUI2 Defines
;--------------------------------

!include "MUI2.nsh"
!define MUI_ABORTWARNING
!define MUI_ICON "${ICON_FILE}"
!define MUI_UNICON "${ICON_FILE}"

; Add checkbox to run application on finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\${EXE_NAME}"
!define MUI_FINISHPAGE_RUN_TEXT "Launch ${APP_NAME}"

;--------------------------------
; Pages
;--------------------------------

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_COMPONENTS ; Use components page for shortcuts
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
; Languages
;--------------------------------

!insertmacro MUI_LANGUAGE "English"

;--------------------------------
; Installer Sections
;--------------------------------

Name "${APP_NAME} ${APP_VERSION}"
OutFile "${OUTPUT_FILENAME}"
InstallDir "$PROGRAMFILES64\${APP_NAME}"
InstallDirRegKey HKLM "Software\${COMPANY_NAME}\${APP_NAME}" "Install_Dir"
ShowInstDetails show

; --- Section Descriptions ---
LangString DESC_Core ${LANG_ENGLISH} "Application Files (Required)"
LangString DESC_DesktopShortcut ${LANG_ENGLISH} "Create Desktop Shortcut"
LangString DESC_StartMenuShortcut ${LANG_ENGLISH} "Create Start Menu Shortcut"

; --- Sections ---
Section "!$(DESC_Core)" SEC_CORE
  SectionIn RO ; Required section
  SetOutPath "$INSTDIR"
  
  ; Files to install
  ; Copy all files from the build directory
  File /r "${BUILD_DIR}\*"
  
  ; Explicitly copy the icon into the install directory so shortcuts can use it
  File "${ICON_FILE}"
  
  ; Store installation folder
  WriteRegStr HKLM "Software\${COMPANY_NAME}\${APP_NAME}" "Install_Dir" "$INSTDIR"
  
  ; Write the uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "$(DESC_StartMenuShortcut)" SEC_START_MENU
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${EXE_NAME}" "" "$INSTDIR\app_logo.ico"
SectionEnd

Section "$(DESC_DesktopShortcut)" SEC_DESKTOP
  CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${EXE_NAME}" "" "$INSTDIR\app_logo.ico"
SectionEnd

;--------------------------------
; Descriptions for Components Page
;--------------------------------
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_CORE} "The core application files."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_START_MENU} "Adds a shortcut to the Start Menu for easy access."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_DESKTOP} "Adds a shortcut to the Desktop for quick launch."
!insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
; Uninstaller Section
;--------------------------------

Section "Uninstall"
  ; Remove registry keys
  DeleteRegKey HKLM "Software\${COMPANY_NAME}\${APP_NAME}"
  DeleteRegKey HKCU "Software\${COMPANY_NAME}\App"

  ; Remove files and directories
  Delete "$INSTDIR\*"
  RMDir /r "$INSTDIR"
  
  ; Remove shortcuts
  Delete "$SMPROGRAMS\${APP_NAME}\*.*"
  RMDir "$SMPROGRAMS\${APP_NAME}"
  Delete "$DESKTOP\${APP_NAME}.lnk"
  
SectionEnd